from sqlalchemy.orm import Session
from app.models import Specialty
from sqlalchemy import select
from app.utils.error_handler import ErrorHandler


class SpecialtyController:
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self):
        query = select(Specialty).order_by(Specialty.title.asc())
        result = await self.db.execute(query)
        return result.scalars().all()

    # validations
    async def check_specialty_exists(self, id: int, error_list: list[str] = []):
        query = select(Specialty).where(Specialty.id == id)
        result = await self.db.execute(query)
        specialty = result.scalar_one_or_none()

        if not specialty:
            error_list.append("Specialty not found.")
