from fastapi import APIRouter, Depends, Path
from jose import jwt
from app.schemas import IRegisterUser, ILogin
from sqlalchemy.orm import Session
from app.utils.error_handler import ErrorHandler
from app.utils.token_operator import token_generator
from app.database import get_db
from app.controllers.request import RequestController
from app.controllers.lawyer import LawyerController
from app.utils.password_operator import get_password_hash, verify_password, validate_password_pattern


router = APIRouter()


@router.get("/all")
async def get_requests_route(db: Session = Depends(get_db)):
    try:
        request_controller = RequestController(db)
        requests = request_controller.get_all()
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return requests


@router.get("/{id}")
async def get_request_by_id_route(
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of request to return")):
    try:
        request_controller = RequestController(db)
        request = request_controller.get_by_id(id)
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    if not request:
        ErrorHandler.not_found("Request")

    return request
