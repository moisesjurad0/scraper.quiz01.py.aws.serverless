from fastapi import APIRouter

from .endpoints import questions

router = APIRouter()
router.include_router(questions.router, prefix="/questions", tags=["Questions"])