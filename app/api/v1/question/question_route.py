from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.error_handler import ErrorHandler
from app.db.base import get_db
from typing import Annotated
from app.dependencies import get_current_user
from app.api.v1.question.question_controller import QuestionController
from app.api.v1.question.answer_controller import AnswerController
from app.schemas import ICreateQuestionBody, ICreateQuestionController, ISecureUser


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


# # get all questions
# @router.get("/all")
# async def get_questions_route(db: AsyncSession = Depends(get_db)):
#     try:
#         question_controller = QuestionController(db)
#         questions = question_controller.get_all()
#         db.close()
#     except Exception as e:
#         ErrorHandler.internal_server_error(e)

#     return questions


# # get question by ID
# @router.get("/{id}")
# async def get_question_by_id_route(
#         db: AsyncSession = Depends(get_db),
#         id: int = Path(description="This is ID of question to return")):
#     try:
#         question_controller = QuestionController(db)
#         question = question_controller.get_by_id(id)
#         db.close()
#     except Exception as e:
#         ErrorHandler.internal_server_error(e)

#     if not question:
#         ErrorHandler.not_found("Question")

#     return question


# # delete question
# @router.delete("/{id}")
# async def delete_question_by_id_route(
#         request: Request,
#         db: AsyncSession = Depends(get_db),
#         id: int = Path(description="This is ID of question to delete")):
#     try:
#         user_id = request.user_id
#         question_controller = QuestionController(db)

#         # check user_id
#         question = question_controller.get_by_id(id)
#         if user_id != question.user_id:
#             ErrorHandler.access_denied("Question")
#             return

#         question = question_controller.delete(id)
#         db.close()
#     except Exception as e:
#         ErrorHandler.internal_server_error(e)

#     return question


# get all categories
@router.get("/category/all")
async def get_question_categories_route(
    db: AsyncSession = Depends(get_db)
):
    question_controller = QuestionController(db)
    categories = await question_controller.get_all_categories()
    return categories


# add answer
@router.post("/{id}/answer")
async def create_answer_route(
    db: AsyncSession = Depends(get_db)
):
    pass


# get question all answers
@router.get("/{question_id}/answer/all")
async def get_question_answers_route(
    question_id: int = Path(
        description="Id of question to return its answers."),
    db: AsyncSession = Depends(get_db)
):
    # TODO check question is not private

    answer_controller = AnswerController(db)
    answers = await answer_controller.get_all(question_id=question_id)
    return answers
