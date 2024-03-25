from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models import City, Province


class CityController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, province_id: int):
        query = select(City).options(joinedload(City.province)
                                     ).filter(City.provinceId == province_id)
        result = await self.db.execute(query)
        return result.scalars().all()
