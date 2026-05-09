from pydantic import BaseModel
from dtos.message import Message
from typing import List


class ChatRequest(BaseModel):
    question: str
    history: List[Message] = []