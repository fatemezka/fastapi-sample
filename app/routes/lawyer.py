from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.utils.error_handler import ErrorHandler
from app.database import get_db
from app.controllers.lawyer import LawyerController

router = APIRouter()


@router.get("/all")
async def get_lawyers_route(db: Session = Depends(get_db)):
    try:
        lawyer_controller = LawyerController(db)
        lawyers = lawyer_controller.get_all()
        db.close()
    except:
        ErrorHandler.internal_server_error()

    return lawyers


@router.get("/{id}")
async def get_lawyer_by_id_route(
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of lawyer to return")):
    try:
        lawyer_controller = LawyerController(db)
        lawyer = lawyer_controller.get_by_id(id)
        db.close()
    except:
        ErrorHandler.internal_server_error()

    if not lawyer:
        ErrorHandler.not_found("Lawyer")
    return lawyer
