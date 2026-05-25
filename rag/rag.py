import os
from langchain_community.vectorstores import Chroma # base de dados vetorial local para armazenar os embeddings e fazer buscas rápidas
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

from rag.document_manager import DocumentManager
from rag.retriever import EnhancedRetriever

# Configurações
CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")
DATA_DIR = os.getenv("DATA_DIR", "data")


MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.2"))
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "models/gemini-embedding-001")
CHROMA_COLLECTION_NAME = os.getenv(
    "CHROMA_COLLECTION_NAME",
    f"evolab_{EMBEDDING_MODEL_NAME.replace('/', '_').replace('-', '_')}",
)

ACTIVE_TEMPLATE_PATH = "rag/prompts/assistant_prompt.txt" 




def get_active_template(path : str = ACTIVE_TEMPLATE_PATH) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Erro Crítico: O ficheiro de prompt '{path}' não foi encontrado. Certifique-se que o caminho está correto e o ficheiro existe.")
        
    with open(path, "r", encoding="utf-8") as f:
        return f.read()






class RAGSystem:
    def __init__(self):

        if not GOOGLE_API_KEY:
            raise RuntimeError("A variável de ambiente GOOGLE_API_KEY é obrigatória para usar o Gemini.")

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            google_api_key=GOOGLE_API_KEY,
        )
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=GEMINI_TEMPERATURE,
            google_api_key=GOOGLE_API_KEY,
        )
        self.vector_store = None
        self.enhanced_retriever = None
        
        self.document_manager = DocumentManager(data_dir=DATA_DIR)
        
        self._initialize_db()




    def _initialize_db(self):
        # Inicializa base dados 
        self.vector_store = Chroma(
            collection_name=CHROMA_COLLECTION_NAME,
            persist_directory=CHROMA_PATH, 
            embedding_function=self.embeddings
        )
        
        # Validar ficheiros já indexados em ChromaDB (através da metadata originada pelo ChromaDB localmente)
        try:
            stored_metadata = self.vector_store.get()["metadatas"]
            processed_files = set(meta.get("source") for meta in stored_metadata if meta and meta.get("source"))
        except Exception:
            processed_files = set()
            
        # Obter os ficheiros novos a indexar
        new_files = self.document_manager.get_new_files(processed_files)
        
        # Processa e adiciona ficheiros novos caso existam
        if new_files:
            chunks = self.document_manager.process_new_documents(new_files)
            if chunks:
                self.vector_store.add_documents(documents=chunks)
                print("Base de vetores atualizada com sucesso.")
        
        self.enhanced_retriever = EnhancedRetriever(vector_store=self.vector_store, k=8)




    def ask(self, context_history: str, question: str) -> str:

        docs = self.enhanced_retriever.get_relevant_documents(question)
        context_text = self.enhanced_retriever.format_context_with_metadata(docs)
        
        active_template = get_active_template()
        prompt = ChatPromptTemplate.from_template(active_template)
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "context": context_text,
            "history": context_history,
            "question": question
        })

        return response.content if hasattr(response, "content") else str(response)
