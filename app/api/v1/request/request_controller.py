from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.utils.error_handler import ErrorHandler
from app.database import Request, RequestSubject
from typing import Optional


class RequestController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Request).all()

    def get_all_subjects(self):
        return self.db.query(RequestSubject).all()

    def get_by_id(self, id: int):
        return self.db.query(Request).filter(Request.id == id).first()

    def create(
            self,
            user_id: int,
            request_type: str,
            request_subject_id: int,
            description: str,
            lawyer_id: Optional[int] = None,
            attachment_1: Optional[str] = None,
            attachment_2:  Optional[str] = None,
            attachment_3:  Optional[str] = None
    ):
        new_request = Request(
            user_id=user_id,
            request_type=request_type,
            request_subject_id=request_subject_id,
            description=description,
            lawyer_id=lawyer_id,
            attachment_1=attachment_1,
            attachment_2=attachment_2,
            attachment_3=attachment_3
        )
        self.db.add(new_request)
        self.db.commit()
        self.db.refresh(new_request)
        return new_request

    def delete(self, id: int):
        request = self.db.query(Request).filter(Request.id == id).first()
        self.db.delete(request)
        self.db.commit()
        return request
