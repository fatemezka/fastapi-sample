from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.user import get_users

router = APIRouter()


@router.get("/all")
async def get_users_route(db: Session = Depends(get_db)):
    return get_users(db)
