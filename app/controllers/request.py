from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.utils.error_handler import ErrorHandler
from app.database import Request
from typing import Optional


class RequestController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Request).all()

    def get_by_id(self, user_id: int):
        return self.db.query(Request).filter(Request.id == user_id).first()
