from pydantic import BaseModel

class Message(BaseModel):
    role: str # Pode ser "user" ou "bot"
    content: str
