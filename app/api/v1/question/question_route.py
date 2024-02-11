from fastapi import APIRouter, Depends, Path
from app.schemas import ICreateQuestion
from sqlalchemy.orm import Session
from app.utils.error_handler import ErrorHandler
from app.database import get_db
from app.api.v1.question.question_controller import QuestionController


router = APIRouter()


@router.get("/all")
async def get_questions_route(db: Session = Depends(get_db)):
    try:
        question_controller = QuestionController(db)
        questions = question_controller.get_all()
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return questions


@router.get("/category/all")
async def get_question_categories_route(db: Session = Depends(get_db)):
    try:
        question_controller = QuestionController(db)
        question_categories = question_controller.get_all_categories()
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return question_categories


@router.get("/{id}")
async def get_question_by_id_route(
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of question to return")):
    try:
        question_controller = QuestionController(db)
        question = question_controller.get_by_id(id)
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    if not question:
        ErrorHandler.not_found("Question")

    return question


@router.post("/")
async def create_question_route(data: ICreateQuestion, db: Session = Depends(get_db)):
    try:
        # user_id = question.user.id  # TODO middleware
        user_id = 1  # TODO remove
        question_controller = QuestionController(db)

        question = question_controller.create(
            user_id=user_id,
            question_category_id=data.question_category_id,
            description=data.description,
            is_private=data.is_private,
            lawyer_id=data.lawyer_id or None
        )

        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return question


@router.delete("/{id}")
async def create_question_by_id_route(
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of question to delete")):

    # user_id = question.user.id  # TODO middleware
    user_id = 1  # TODO remove
    question_controller = QuestionController(db)

    # check user_id
    question = question_controller.get_by_id(id)
    if user_id != question.user_id:
        ErrorHandler.access_denied("Question")

    try:
        question = question_controller.delete(id)
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return question
