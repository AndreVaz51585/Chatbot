from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from rag import RAGSystem

# Inicialização da API
app = FastAPI(title="OpenEvolve Chatbot API")

# Ligar CORS para permitir que sites externos utilizem a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização do RAG com LLM e Vector Database
rag = RAGSystem()

# Estruturas de dados (Pydantic) para tipagem forte dos requests da API
class Message(BaseModel):
    role: str # Pode ser "user" ou "bot"
    content: str

class ChatRequest(BaseModel):
    question: str
    history: List[Message] = []

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    # Formatar o histórico de mensagens numa única String
    history_text = ""
    for msg in request.history:
        history_text += f"{msg.role.capitalize()}: {msg.content}`n"
        
    print(f"-> Pedido RAG recebido: {request.question}")
    
    # Chamar o nosso módulo de RAG que vai à DB e contacta o LLM
    answer = rag.ask(context_history=history_text, question=request.question)
    
    return {"reply": answer}

# Servir ficheiros estáticos (HTML, CSS, JS) para o frontend
import os
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    # O Ponto de entrada que serve a página
    return FileResponse("static/index.html")

