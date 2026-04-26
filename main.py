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
    allow_origins=[  
        "http://localhost:5173",
        "http://127.0.0.1:5173"], # permite somente front-end especificos. 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização do RAG com LLM e Vector Database
rag = RAGSystem()

# Estruturas de dados (Pydantic) para tipagem forte dos requests da API
# O BaseModel é usado para fazer parsing de objetos JSON para python e validação automática dos dados recebidos.
# Além disso, facilita a documentação automática da API com OpenAPI/Swagger, mostrando claramente os campos esperados e seus tipos.
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
        # Está a especificar o formato [ {role: "user", content: "Olá"}]
        
        
        
    print(f"-> Pedido RAG recebido: {request.question}")
    
    # Chamar o nosso módulo de RAG que vai à DB e contacta o LLM
    answer = rag.ask(context_history=history_text, question=request.question)
    
    return {"reply": answer}

# Servir ficheiros estáticos (HTML, CSS, JS) para o frontend
import os
os.makedirs("static", exist_ok=True) # cria a diretoria /static se não existir
# liga a pasta /static e serve os ficheiros lá dentro. Assim, quando o front-end pedir /static/index.html, ele vai buscar o ficheiro na pasta local static/index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    # O Ponto de entrada que serve a página
    return FileResponse("static/index.html")

