from fastapi import APIRouter, Depends, Path, Request
from app.schemas import ICreateQuestion, ICreateAnswer
from sqlalchemy.orm import Session
from app.utils.error_handler import ErrorHandler
from app.db.base import get_db
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


@router.get("/{id}/answer/all")
async def get_question_answers_route(
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of question to return its answers")):
    try:
        question_controller = QuestionController(db)
        question_answers = question_controller.get_question_all_answers(
            question_id=id)
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return question_answers


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
async def create_question_route(
        request: Request,
        data: ICreateQuestion,
        db: Session = Depends(get_db)):
    try:
        user_id = request.user_id
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


@router.post("/{id}/answer")
async def create_answer_route(
        request: Request,
        data: ICreateAnswer,
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of question to create an answer for it")):
    try:
        lawyer_id = request.lawyer_id
        question_controller = QuestionController(db)

        answer = question_controller.create_answer(
            lawyer_id=lawyer_id,
            question_id=id,
            description=data.description
        )

        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return answer


@router.delete("/{id}")
async def delete_question_by_id_route(
        request: Request,
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of question to delete")):
    try:
        user_id = request.user_id
        question_controller = QuestionController(db)

        # check user_id
        question = question_controller.get_by_id(id)
        if user_id != question.user_id:
            ErrorHandler.access_denied("Question")
            return

        question = question_controller.delete(id)
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return question
