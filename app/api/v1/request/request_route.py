from fastapi import APIRouter, Depends, Path, Request, Query
from app.schemas import ICreateRequest
from sqlalchemy.orm import Session
from app.utils.error_handler import ErrorHandler
from app.db.base import get_db
from app.api.v1.request.request_controller import RequestController


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


@router.get("/subject/all")
async def get_request_subjects_route(
        db: Session = Depends(get_db),
        request_type: str = Query(None)):
    try:
        request_controller = RequestController(db)
        request_subjects = request_controller.get_all_subjects(
            request_type=request_type)
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return request_subjects


@router.get("/{id}")
async def get_request_by_id_route(
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of request to return")):
    try:
        request_controller = RequestController(db)
        request_ = request_controller.get_by_id(id)
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    if not request_:
        ErrorHandler.not_found("Request")

    return request_


@router.post("/")
async def create_request_route(
        request: Request,
        data: ICreateRequest,
        db: Session = Depends(get_db)):
    try:
        user_id = request.user_id
        request_controller = RequestController(db)

        request_ = request_controller.create(
            user_id=user_id,
            request_type=data.request_type,
            request_subject_id=data.request_subject_id,
            description=data.description,
            lawyer_id=data.lawyer_id or None,
            attachment_1=data.attachment_1 or None,
            attachment_2=data.attachment_2 or None,
            attachment_3=data.attachment_3 or None
        )

        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return request_


@router.delete("/{id}")
async def create_request_by_id_route(
        request: Request,
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of request to delete")):
    try:
        user_id = request.user_id
        request_controller = RequestController(db)

        # check user_id
        request_ = request_controller.get_by_id(id)
        if user_id != request_.user_id:
            ErrorHandler.access_denied("Request")
            return

        request_ = request_controller.delete(id)
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return request_
