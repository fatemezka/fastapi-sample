from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import City, Province


class CityController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, province_id: int):
        # cities = (await self.db.execute(select(City).filter(City.provinceId == province_id))).scalars().all()
        # return cities
        query = select(City).join(Province).filter(
            City.provinceId == province_id)
        result = await self.db.execute(query)
        cities_with_province = result.scalars().all()
        return cities_with_province
