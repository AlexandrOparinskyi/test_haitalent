from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Question(Base):
    __tablename__ = "questions"

    text: Mapped[str] = mapped_column(Text, nullable=False)

    answers: Mapped[list["Answer"]] = relationship("Answer",
                                                   back_populates="question",
                                                   lazy="selectin")
