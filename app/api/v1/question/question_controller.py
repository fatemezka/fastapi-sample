from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.utils.error_handler import ErrorHandler
from app.models import Question, QuestionCategory, Answer
from app.schemas import ICreateQuestionController


class QuestionController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        questions = (await self.db.execute(select(Question))).scalars().all()
        return questions

    def get_by_id(self, id: int):
        return self.db.query(Question).filter(Question.id == id).first()

    async def get_all_categories(self):
        categories = (await self.db.execute(select(QuestionCategory))).scalars().all()
        return categories

    def get_question_all_answers(self, question_id: int):
        return self.db.query(Answer).filter(Answer.question_id == question_id).all()

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

    async def delete(self, id: int):
        question = self.db.query(Question).filter(Question.id == id).first()
        self.db.delete(question)
        self.db.commit()
        return question

    # validations
    async def check_category_exists(self, category_id: int, error_list: list[str] = []):
        category = (await self.db.execute(select(QuestionCategory).where(QuestionCategory.id == category_id))).scalar_one_or_none()
        if not category:
            error_list.append("Category does not exist.")
