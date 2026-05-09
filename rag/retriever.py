from typing import List
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

class EnhancedRetriever:
    """
    Classe responsável por encapsular a Vector Store e formatar o contexto 
    para o LLM, garantindo a sua metadata (nome dos ficheiros/origem).
    """
    def __init__(self, vector_store, k: int = 5):
        self.retriever: VectorStoreRetriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )

    def get_relevant_documents(self, query: str) -> List[Document]:
        """Recupera os documentos mais relevantes."""
        return self.retriever.invoke(query)

    def format_context_with_metadata(self, docs: List[Document]) -> str:
        """
        Gera um bloco de texto contendo os chunks recuperados associados aos metadados,
        para que o LLM saiba a origem das informações.
        """
        context_parts = []
        for doc in docs:
            # A fonte (source) e página (page) vêm por norma na propriedade metadata criada pelos Loaders do LangChain
            source = doc.metadata.get("source", "Documento Desconhecido")
            page = doc.metadata.get("page", "")
            
            meta_info = f"Origem: {source}"
            if page:
                meta_info += f" (Página {page})"
                
            context_part = f"[{meta_info}]\n{doc.page_content}"
            context_parts.append(context_part)
            
        return "\n\n---\n\n".join(context_parts)
