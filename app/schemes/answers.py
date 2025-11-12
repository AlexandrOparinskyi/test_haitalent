import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AnswerCreateModel(BaseModel):
    user_id: uuid.UUID = Field(description="User id")
    text: str = Field(min_length=1, description="Answer text")


class AnswerModel(BaseModel):
    id: int
    question_id: int
    user_id: uuid.UUID
    text: str
    created_at: datetime
