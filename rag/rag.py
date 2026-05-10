import os
from langchain_huggingface import HuggingFaceEmbeddings # modelo que transforma texto em vetores numéricos (embeddings)
from langchain_community.vectorstores import Chroma # base de dados vetorial local para armazenar os embeddings e fazer buscas rápidas
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from rag.document_manager import DocumentManager
from rag.retriever import EnhancedRetriever

# Configurações
CHROMA_PATH = "chroma_db"
DATA_DIR = "data" 


#MODEL_NAME = "qwen2.5-coder:14b"
MODEL_NAME = "llama3"
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

ACTIVE_TEMPLATE_PATH = "rag/prompts/assistant_prompt.txt" 




def get_active_template(path : str = ACTIVE_TEMPLATE_PATH) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Erro Crítico: O ficheiro de prompt '{path}' não foi encontrado. Certifique-se que o caminho está correto e o ficheiro existe.")
        
    with open(path, "r", encoding="utf-8") as f:
        return f.read()






class RAGSystem:
    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        self.llm = OllamaLLM(model=MODEL_NAME) 
        self.vector_store = None
        self.enhanced_retriever = None
        
        self.document_manager = DocumentManager(data_dir=DATA_DIR)
        
        self._initialize_db()




    def _initialize_db(self):
        # Inicializa base dados 
        self.vector_store = Chroma(
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
        
        return chain.invoke({
            "context": context_text,
            "history": context_history,
            "question": question
        })

