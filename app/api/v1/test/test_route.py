from fastapi import APIRouter
from app.db.base import get_db

router = APIRouter()


@router.get("/all")
async def get_tests_route():
    return ["test1", "test2"]
