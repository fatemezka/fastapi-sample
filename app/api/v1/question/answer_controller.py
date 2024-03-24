from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.utils.error_handler import ErrorHandler
from app.models import Answer


class AnswerController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, question_id: int):
        query = select(Answer).filter(Answer.questionId == question_id)
        result = await self.db.execute(query)
        answers = result.scalars().all()
        return answers

    async def create(self, answer_items):
        pass
