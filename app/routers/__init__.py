from fastapi import FastAPI

from .questions import questions_router
from .answers import answers_router


def register_routers(router: FastAPI) -> None:
    router.include_router(questions_router)
    router.include_router(answers_router)
