from typing import List, Optional

from pydantic import BaseModel


class ErrorDetailSchema(BaseModel):
    field: Optional[str] = None
    message: str
    code: Optional[str] = None


class ErrorResponseSchema(BaseModel):
    message: str
    details: Optional[List[ErrorDetailSchema]] = None
