from sqlalchemy.orm import Session
from app.models import Lawyer, User
from sqlalchemy.exc import SQLAlchemyError
from app.utils.error_handler import ErrorHandler
from app.api.v1.user.user_controller import UserController
from typing import Optional


class LawyerController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Lawyer).all()

    def get_by_id(self, lawyer_id: int):
        return self.db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()

    def get_by_user_id(self, user_id: int):
        return self.db.query(Lawyer).filter(Lawyer.user_id == user_id).first()

    def get_by_id_and_user_id(self, id: int, user_id: int):
        return self.db.query(Lawyer).filter(Lawyer.id == id, Lawyer.user_id == user_id).first()

    def get_by_license_code(self, license_code: str):
        return self.db.query(Lawyer).filter(Lawyer.license_code == license_code).first()

    def create(
        self,
        username: str,
        name: str,
        family: str,
        phone_number: str,
        hashed_password: str,
        age: int,
        sex: str,
        province_id: int,
        city_id: int,
        edu_degree: str,
        study_field: str,
        license_code: str,
        position: str,
        experience_years: int,
        biography: str,
        email: Optional[str] = None,
        marital_status:  Optional[str] = None,
        profile_photo:  Optional[str] = None,
        office_phone_number:  Optional[str] = None,
        office_address:  Optional[str] = None
    ):
        # first create user
        # new_user = User(
        #     is_lawyer=True,
        #     username=username,
        #     name=name,
        #     family=family,
        #     phone_number=phone_number,
        #     hashed_password=hashed_password,
        #     email=email,
        #     marital_status=marital_status,
        #     age=age,
        #     sex=sex,
        #     province_id=province_id,
        #     city_id=city_id,
        #     profile_photo=profile_photo
        # )
        # self.db.add(new_user)
        # self.db.refresh(new_user)
        # self.db.flush()
        user_controller = UserController(self.db)
        new_user = user_controller.create(
            is_lawyer=True,
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

        # then create lawyer
        new_lawyer = Lawyer(
            user_id=new_user.id,
            edu_degree=edu_degree,
            study_field=study_field,
            license_code=license_code,
            position=position,
            experience_years=experience_years,
            biography=biography,
            office_phone_number=office_phone_number,
            office_address=office_address
        )
        self.db.add(new_lawyer)
        self.db.commit()
        return {
            "user": new_user,
            "lawyer": new_lawyer
        }
