import logging

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session, Question
from ..schemes import QuestionCreateModel, QuestionModel, QuestionsModel

questions_router = APIRouter(prefix="/questions",
                             tags=["questions"])
logger = logging.getLogger(__name__)


@questions_router.get("/",
                      status_code=status.HTTP_200_OK,
                      response_model=list[QuestionsModel])
async def get_questions(session: AsyncSession = Depends(get_async_session)):
    try:
        questions = await session.scalars(select(Question))
        return questions.all()
    except Exception as err:
        logger.error(f"Failed to fetch questions: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to fetch questions. "
                                   "Try again later")


@questions_router.get("/{q_id}",
                      status_code=status.HTTP_200_OK,
                      response_model=QuestionModel)
async def get_question(q_id: int,
                       session: AsyncSession = Depends(get_async_session)):
    try:
        question = await session.scalar(select(Question).where(
            Question.id == q_id
        ))

        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Failed to fetch question "
                                       f"with id {q_id}")

        return question
    except Exception as err:
        logger.error(f"Failed to fetch question with id {q_id}: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to fetch question. "
                                   "Try again later")


@questions_router.post("/",
                       status_code=status.HTTP_201_CREATED,
                       response_model=QuestionModel | None)
async def create_question(question: QuestionCreateModel,
                          session: AsyncSession = Depends(get_async_session)):
    try:
        query = await session.execute(insert(Question).values(
            text=question.text
        ).returning(Question))
        await session.commit()
        return query.scalar_one_or_none()
    except Exception as err:
        logger.error(f"Failed to create question: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to create question. "
                                   "Try again later")


@questions_router.delete('/{q_id}',
                         status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(q_id: int,
                          session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(delete(Question).where(
            Question.id == q_id
        ))
        await session.commit()
    except Exception as err:
        logger.error(f"Failed to delete question: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to delete question. "
                                   "Try again later")
