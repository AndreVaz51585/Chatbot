import os
import glob
from typing import List, Set
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentManager:
    """Classe responsável por gerir os documentos: detetar novos ficheiros, carregá-los e dividi-los em chunks para indexação."""

    def __init__(self, data_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.data_dir = data_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Garante que a diretoria existe
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
            
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def get_supported_files(self) -> List[str]:
        """Procura de forma recursiva por todos os ficheiros suportados na diretoria."""
        supported_extensions = ('*.txt', '*.md', '*.pdf')
        files = []
        for ext in supported_extensions:
            # glob com recursive=True permite procurar em subpastas
            files.extend(glob.glob(os.path.join(self.data_dir, '**', ext), recursive=True))
        return files


    def get_new_files(self, processed_files: Set[str]) -> List[str]:
        """Deteta novos ficheiros que ainda não foram processados (ainda não estão na base de dados)."""
        all_files = self.get_supported_files()
        return [f for f in all_files if f not in processed_files]

    def load_document(self, file_path: str) -> List[Document]:
        """Seleciona o parser correto com base na extensão do ficheiro."""
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == '.pdf':
                loader = PyPDFLoader(file_path)
            elif ext in ['.txt', '.md']:
                loader = TextLoader(file_path, encoding="utf-8")
            else:
                print(f"Formato não suportado: {file_path}")
                return []
            
            return loader.load()
        except Exception as e:
            print(f"Erro ao carregar o documento {file_path}: {e}")
            return []

    def process_new_documents(self, new_files: List[str]) -> List[Document]:
        """Carrega e divide (chunks) os novos ficheiros."""
        if not new_files:
            return []
            
        print(f"A processar {len(new_files)} novos documentos...")
        all_documents = []
        for file in new_files:
            docs = self.load_document(file)
            all_documents.extend(docs)
            
        # Dividir os documentos de forma recursiva
        chunks = self.text_splitter.split_documents(all_documents)
        print(f"Foram gerados {len(chunks)} chunks de contexto.")
        return chunks
