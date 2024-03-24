from sqlalchemy.orm import Session
from app.models import Lawyer, User
from sqlalchemy import select
from app.utils.error_handler import ErrorHandler
from app.api.v1.user.user_controller import UserController


class LawyerController:
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self):  # TODO filters
        lawyers = (await self.db.execute(select(Lawyer))).scalars().all()
        return lawyers

    async def get_by_id(self, id: int):
        lawyer = (await self.db.execute(select(Lawyer).where(Lawyer.id == id))).scalar_one_or_none()
        if not lawyer:
            raise ErrorHandler.not_found("Lawyer")
        return lawyer

    async def get_by_user_id(self, user_id: int):
        lawyer = (await self.db.execute(select(Lawyer).where(Lawyer.userId == user_id))).scalar_one_or_none()
        if not lawyer:
            raise ErrorHandler.not_found("Lawyer")
        return lawyer

    # validations
    async def check_license_code_not_exists(self, license_code: str, error_list: list[str] = []):
        lawyer = (await self.db.execute(select(Lawyer).where(Lawyer.licenseCode == license_code))).scalar_one_or_none()
        if lawyer:
            error_list.append("License code does exist.")
