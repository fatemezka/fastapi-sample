from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from app.utils.error_handler import ErrorHandler
from app.models import Question, QuestionCategory, Answer
from app.schemas import ICreateQuestionController


class QuestionController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, category_id: int, is_private: bool):
        query = select(Question).options(joinedload(Question.questionCategory)).filter(
            Question.isPrivate == is_private)
        if category_id:
            query = query.filter(Question.questionCategoryId == category_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id: int):
        query = select(Question).options(joinedload(
            Question.questionCategory)).where(Question.id == id)
        result = await self.db.execute(query)
        question = result.scalar_one_or_none()

        if not question:
            raise ErrorHandler.not_found("Question")
        return question

    async def get_all_categories(self):
        query = select(QuestionCategory)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, question_items: ICreateQuestionController):
        async with self.db as async_session:
            new_question = Question(
                userId=question_items["userId"],
                lawyerId=None,
                questionCategoryId=question_items["questionCategoryId"],
                description=question_items["description"],
                isPrivate=question_items["isPrivate"]
            )
            async_session.add(new_question)
            await async_session.commit()
            await async_session.refresh(new_question)
            return new_question

    async def delete_by_id(self, id: int):
        question = await self.get_by_id(id=id)
        if question:
            # Delete associated answers first
            await self.db.execute(delete(Answer).where(Answer.questionId == id))
            # Now delete the question
            await self.db.execute(delete(Question).where(Question.id == id))

            await self.db.commit()
        return

    # validations
    async def check_category_exists(self, category_id: int, error_list: list[str] = []):
        query = select(QuestionCategory).where(
            QuestionCategory.id == category_id)
        result = await self.db.execute(query)
        category = result.scalar_one_or_none()
        if not category:
            error_list.append("Category does not exist.")

    async def check_question_exists(self, question_id: int, error_list: list[str] = []):
        try:
            question = await self.get_by_id(id=question_id)
        except Exception:
            error_list.append("Question does not exist.")
