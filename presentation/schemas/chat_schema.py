from typing import Any, Dict, List

from presentation.schemas.bases.base import BaseSchema


class ChatResponseSchema(BaseSchema):
    user_id: int
    response: Dict[str, Any]
    history: List[str]


class ChatHistoryResponseSchema(BaseSchema):
    user_id: int
    history: List[str]


class ChatInputSchema(BaseSchema):
    message: str
