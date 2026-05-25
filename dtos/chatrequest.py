from pydantic import BaseModel, Field
from dtos.message import Message
from typing import List


class ChatRequest(BaseModel):
    question: str
    history: List[Message] = Field(default_factory=list)
