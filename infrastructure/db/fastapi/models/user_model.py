from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str
    active: bool = Field(
        default=True,
        description="Indicates if the user is active",
    )
    is_superuser: bool = Field(
        default=False, description="Indicates if the user has superuser privileges"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the user was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the user was last updated",
    )
    created_by: Optional[int] = Field(
        default=None,
        foreign_key="user.id",
        description="ID of the user who created this record",
    )
    updated_by: Optional[int] = Field(
        default=None,
        foreign_key="user.id",
        description="ID of the user who last updated this record",
    )
