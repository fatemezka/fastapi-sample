from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.utils.error_handler import ErrorHandler
from app.database import User
from typing import Optional


class UserController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_phone_number(self, phone_number: str):
        return self.db.query(User).filter(User.phone_number == phone_number).first()

    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(
        self,
        is_lawyer: bool,
        username: str,
        name: str,
        family: str,
        phone_number: str,
        hashed_password: str,
        email: Optional[str] = None,
        marital_status: Optional[str] = None,
        age: Optional[int] = None,
        sex: Optional[str] = None,
        province_id: Optional[int] = None,
        city_id: Optional[int] = None,
        profile_photo: Optional[str] = None
    ):
        new_user = User(
            is_lawyer=is_lawyer,
            username=username,
            name=name,
            family=family,
            phone_number=phone_number,
            email=email,
            marital_status=marital_status,
            age=age,
            sex=sex,
            province_id=province_id,
            city_id=city_id,
            hashed_password=hashed_password,
            profile_photo=profile_photo
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
