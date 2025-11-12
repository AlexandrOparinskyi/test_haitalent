from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.schemes import AnswerModel


class QuestionCreateModel(BaseModel):
    text: str = Field(min_length=1, description="Question text")


class QuestionsModel(BaseModel):
    id: int
    text: str
    created_at: datetime


class QuestionModel(BaseModel):
    id: int
    text: str
    answers: list[AnswerModel]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
