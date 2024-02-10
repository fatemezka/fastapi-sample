from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.utils.error_handler import ErrorHandler
from app.database import get_db
from app.controllers.user import UserController

router = APIRouter()


@router.get("/all")
async def get_users_route(db: Session = Depends(get_db)):
    try:
        user_controller = UserController(db)
        users = user_controller.get_all()
        db.close()
    except:
        ErrorHandler.internal_server_error()

    return users


@router.get("/{id}")
async def get_user_by_id_route(
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of user to return")):
    try:
        user_controller = UserController(db)
        user = user_controller.get_by_id(id)
        db.close()
    except:
        ErrorHandler.internal_server_error()

    if not user:
        ErrorHandler.not_found("User")

    return user
