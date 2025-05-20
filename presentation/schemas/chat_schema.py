from typing import Any, Dict, List

from ninja import Schema
from pydantic import BaseModel


class ChatResponseSchema(Schema):
    user_id: int
    response: Dict[str, Any]
    history: List[str]


class ChatHistoryResponseSchema(Schema):
    user_id: int
    history: List[str]


class ChatInputSchema(BaseModel):
    message: str
