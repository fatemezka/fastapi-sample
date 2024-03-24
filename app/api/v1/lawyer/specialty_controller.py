from sqlalchemy.orm import Session
from app.models import Specialty
from sqlalchemy import select
from app.utils.error_handler import ErrorHandler


class SpecialtyController:
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self):
        lawyers = (await self.db.execute(select(Specialty))).scalars().all()
        return lawyers

    # validations
    async def check_specialty_exists(self, id: int, error_list: list[str] = []):
        specialty = (await self.db.execute(select(Specialty).where(Specialty.id == id))).scalar_one_or_none()
        if not specialty:
            error_list.append("Specialty not found.")
