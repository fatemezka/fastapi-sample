from fastapi import APIRouter, Depends, Path, Body, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.error_handler import ErrorHandler
from app.db.base import get_db
from typing import Annotated
from app.dependencies import get_current_user
from app.api.v1.question.question_controller import QuestionController
from app.api.v1.question.answer_controller import AnswerController
from app.api.v1.lawyer.lawyer_controller import LawyerController
from app.schemas import ICreateQuestionBody, ICreateQuestionController, ISecureUser, ICreateAnswerBody


router = APIRouter()


# add question
@router.post("/")
async def create_question_route(
    current_user: Annotated[ISecureUser, Depends(get_current_user)],
    data: ICreateQuestionBody = Body(description="New question fields"),
    db: AsyncSession = Depends(get_db)
):
    error_list = []
    question_controller = QuestionController(db)

    # check questionCategoryId
    await question_controller.check_category_exists(category_id=data.questionCategoryId, error_list=error_list)

    if error_list:
        raise ErrorHandler.bad_request(custom_message={"errors": error_list})

    question_items = {
        "userId": current_user.id,
        "questionCategoryId": data.questionCategoryId,
        "description": data.description,
        "isPrivate": data.isPrivate
    }
    question = await question_controller.create(question_items=question_items)
    await db.close()

    return question


# get all questions
@router.get("/all")
async def get_all_questions_route(
    category_id: int = Query(
        default=None, description="Id of question category to return its questions."),
    db: AsyncSession = Depends(get_db)
):
    question_controller = QuestionController(db)
    questions = await question_controller.get_all(category_id=category_id, is_private=False)
    await db.close()

    return questions


# get question by ID
@router.get("/{question_id}")
async def get_question_by_id_route(
    question_id: int = Path(description="Id of question to return."),
    db: AsyncSession = Depends(get_db)
):
    question_controller = QuestionController(db)
    question = await question_controller.get_by_id(id=question_id)
    await db.close()

    return question


# delete question
@router.delete("/{question_id}")
async def delete_question_by_id_route(
    current_user: Annotated[ISecureUser, Depends(get_current_user)],
    question_id: int = Path(description="Id of question to delete."),
    db: AsyncSession = Depends(get_db)
):
    question_controller = QuestionController(db)
    question = await question_controller.get_by_id(id=question_id)

    if question.userId != current_user.id:
        raise ErrorHandler.access_denied("Question")

    await question_controller.delete_by_id(id=question_id)
    await db.close()

    return {"message": "Question deleted successfully"}


# get all categories
@router.get("/category/all")
async def get_question_categories_route(
    db: AsyncSession = Depends(get_db)
):
    question_controller = QuestionController(db)
    categories = await question_controller.get_all_categories()
    await db.close()
    return categories


# add answer
@router.post("/{question_id}/answer")
async def create_answer_route(
    current_user: Annotated[ISecureUser, Depends(get_current_user)],
    question_id: int = Path(description="Id of question to add an answer."),
    data: ICreateAnswerBody = Body(description="New answer fields"),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.isLawyer:
        raise ErrorHandler.access_denied("Answer the question.")

    error_list = []
    answer_controller = AnswerController(db)
    question_controller = QuestionController(db)
    lawyer_controller = LawyerController(db)

    # check questionId
    await question_controller.check_question_exists(question_id=question_id, error_list=error_list)

    # check lawyer
    lawyer = await lawyer_controller.get_by_user_id(user_id=current_user.id, error_list=error_list)

    if error_list:
        raise ErrorHandler.bad_request(custom_message={"errors": error_list})

    answer_items = {
        "lawyerId": lawyer.id,
        "questionId": data.questionId,
        "description": data.description
    }
    answer = await answer_controller.create(answer_items=answer_items)
    await db.close()

    return answer


# get question all answers
@router.get("/{question_id}/answer/all")
async def get_question_answers_route(
    question_id: int = Path(
        description="Id of question to return its answers."),
    db: AsyncSession = Depends(get_db)
):
    answer_controller = AnswerController(db)
    answers = await answer_controller.get_all(question_id=question_id)
    await db.close()

    return answers
