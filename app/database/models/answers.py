import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Answer(Base):
    __tablename__ = "answers"

    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id",
                                                        ondelete="cascade"),
                                             nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                               nullable=False,
                                               default=uuid.uuid4)
    text: Mapped[str] = mapped_column(Text)

    question: Mapped["Question"] = relationship("Question",
                                                back_populates="answers")
