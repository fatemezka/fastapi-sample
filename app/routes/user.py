from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.user import get_users, get_user_by_id

router = APIRouter()


@router.get("/all")
async def get_users_route(db: Session = Depends(get_db)):
    users = get_users(db)
    db.close()
    return users


@router.get("/{user_id}")
async def get_users_route(
        db: Session = Depends(get_db),
        user_id: int = Path(description="This is ID of user to return")):
    user = get_user_by_id(db, user_id)
    db.close()
    return user
