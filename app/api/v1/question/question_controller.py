from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.utils.error_handler import ErrorHandler
from app.database import Question, QuestionCategory
from typing import Optional


class QuestionController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Question).all()

    def get_all_categories(self):
        return self.db.query(QuestionCategory).all()

    def get_by_id(self, id: int):
        return self.db.query(Question).filter(Question.id == id).first()

    def create(
            self,
            user_id: int,
            question_category_id: int,
            description: str,
            is_private: bool,
            lawyer_id: Optional[int] = None,
    ):
        new_question = Question(
            user_id=user_id,
            question_category_id=question_category_id,
            description=description,
            is_private=is_private,
            lawyer_id=lawyer_id,
        )
        self.db.add(new_question)
        self.db.commit()
        self.db.refresh(new_question)
        return new_question

    def delete(self, id: int):
        question = self.db.query(Question).filter(Question.id == id).first()
        self.db.delete(question)
        self.db.commit()
        return question
