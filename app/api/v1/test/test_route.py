from typing import Annotated
from fastapi import APIRouter, Depends
from app.db.base import get_db
from app.models import User
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return {"user": current_user}
