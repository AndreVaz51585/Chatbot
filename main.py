from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dtos.chatrequest import ChatRequest
import os

from rag.rag import RAGSystem

app = FastAPI(title="OpenEvolve Chatbot API")



# Ligar CORS para permitir que sites externos utilizem a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[  
        "http://localhost:3000",
        "http://127.0.0.1:3000"], # permite somente front-end especificos. 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGSystem()


@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    # Formatar o histórico de mensagens numa única String
    history_text = ""
    for msg in request.history:
        history_text += f"{msg.role.capitalize()}: {msg.content}`n"
        # Está a especificar o formato [ {role: "user", content: "Olá"}]
        
        
        
    print(f"-> Pedido RAG recebido: {request.question}")
    
    answer = rag.ask(context_history=history_text, question=request.question)
    
    return {"reply": answer}




os.makedirs("static", exist_ok=True) 

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    # O Ponto de entrada que serve a página
    return FileResponse("static/index.html")

