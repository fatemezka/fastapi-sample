from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.utils.error_handler import ErrorHandler
from app.models import Answer
from app.schemas import ICreateAnswerController


class AnswerController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, question_id: int):
        query = select(Answer).filter(Answer.questionId == question_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, answer_items: ICreateAnswerController):
        async with self.db as async_session:
            new_answer = Answer(
                lawyerId=answer_items["lawyerId"],
                questionId=answer_items["questionId"],
                description=answer_items["description"]
            )
            async_session.add(new_answer)
            await async_session.commit()
            await async_session.refresh(new_answer)
            return new_answer
