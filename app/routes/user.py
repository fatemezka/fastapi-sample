from fastapi import APIRouter
from app.controllers.user import get_user, create_user

router = APIRouter()


@router.get("/")
async def get_user_route():
    return "User hahahaha...."


@router.get("/{user_id}")
async def get_user_route(user_id: int):
    return get_user(user_id)


@router.post("/")
async def create_user_route(user_data: dict):
    return create_user(user_data)
