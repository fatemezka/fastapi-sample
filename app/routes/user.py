from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.user import UserController

router = APIRouter()


@router.get("/all")
async def get_users_route(db: Session = Depends(get_db)):
    user_controller = UserController(db)
    users = user_controller.get_all()
    db.close()
    return users


@router.get("/{user_id}")
async def get_user_by_id_route(
        db: Session = Depends(get_db),
        user_id: int = Path(description="This is ID of user to return")):
    user_controller = UserController(db)
    user = user_controller.get_by_id(user_id)
    db.close()
    return user
