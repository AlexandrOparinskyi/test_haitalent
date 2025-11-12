import logging

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session, Answer
from app.schemes import AnswerCreateModel, AnswerModel

answers_router = APIRouter(tags=["answers"])
logger = logging.getLogger(__name__)


@answers_router.get("/answers/{a_id}",
                    status_code=status.HTTP_200_OK,
                    response_model=AnswerModel)
async def get_answer(a_id: int,
                     session: AsyncSession = Depends(get_async_session)):
    try:
        answer = await session.scalar(select(Answer).where(
            Answer.id == a_id
        ))

        if answer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Answer with id {a_id} not found")

        return answer
    except Exception as err:
        logger.error(f"Failed to fetch answer with id {a_id}: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to fetch answer. Try again later")


@answers_router.post("/questions/{q_id}/answers",
                     status_code=status.HTTP_201_CREATED,
                     response_model=AnswerModel | None)
async def create_answer(q_id: int,
                        answer: AnswerCreateModel,
                        session: AsyncSession = Depends(get_async_session)):
    try:
        query = await session.execute(insert(Answer).values(
            question_id=q_id,
            text=answer.text
        ).returning(Answer))
        await session.commit()
        return query.scalar_one_or_none()
    except IntegrityError:
        logger.error(f"Failed to create answer: "
                     f"Question with id {q_id} bot found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Question with id {q_id} not found")
    except Exception as err:
        logger.error(f"Failed to create answer: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to create answer. Try again later")


@answers_router.delete("/answers/{a_id}",
                       status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(a_id: int,
                        session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(delete(Answer).where(Answer.id == a_id))
        await session.commit()
    except Exception as err:
        logger.error(f"Failed to delete answer with id {a_id}: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to delete answer. Try again later")
