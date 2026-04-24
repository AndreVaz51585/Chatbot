import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Configurações
DATA_PATH = "data/knowledge.txt"
CHROMA_PATH = "chroma_db"
MODEL_NAME = "qwen2.5-coder:14b"

class RAGSystem:
    def __init__(self):
        # HuggingFace Embeddings para gerar os vetores (corre localmente)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        self.llm = OllamaLLM(model=MODEL_NAME)
        self.vector_store = None
        self.retriever = None
        
        self._initialize_db()

    def _initialize_db(self):
        # Verifica se a base de dados vetorial já existe
        if os.path.exists(CHROMA_PATH):
            self.vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embeddings)
        else:
            # Caso contrário, carrega o ficheiro e cria os embeddings
            if not os.path.exists(os.path.dirname(DATA_PATH)):
                os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
            if not os.path.exists(DATA_PATH):
                with open(DATA_PATH, "w", encoding="utf-8") as f:
                    f.write("A OpenEvolve é uma plataforma que otimiza processos de IT. "
                            "Permite aos utilizadores experimentar novas ferramentas e "
                            "oferece um dashboard robusto para os gestores administradores.")

            print("A carregar documentos de conhecimento (RAG)...")
            loader = TextLoader(DATA_PATH, encoding="utf-8")
            documents = loader.load()
            
            # Dividir os documentos em blocos mais pequenos (chunks)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = text_splitter.split_documents(documents)
            
            # Guardar os vetores na base de dados Chroma localmente
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=CHROMA_PATH
            )
            
        # Configurar quantas páginas de contexto queremos recuperar de cada vez
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

    def ask(self, context_history: str, question: str) -> str:
        # Recuperar contexto da base de dados vetorial
        docs = self.retriever.invoke(question)
        context_text = "\n\n".join([doc.page_content for doc in docs])
        
       
        template = """És um assistente virtual para a plataforma OpenEvolve.
Responde de forma amigável e profissional e SOMENTE baseado no Contexto da Empresa ou no Histórico da Conversa.
Se não souberes a resposta, diz apenas que não tens a certeza e sugere contactar o suporte.

Contexto da Empresa:
{context}

Histórico da Conversa:
{history}

Pergunta do utilizador: {question}
Tua Resposta:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm
        
        return chain.invoke({
            "context": context_text,
            "history": context_history,
            "question": question
        })
