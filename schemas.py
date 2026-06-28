from datetime import datetime
from uuid import uuid4, UUID

from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class Todo(BaseModel):
    id: UUID
    title: str
    completed: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}
