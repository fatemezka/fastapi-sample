from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Province


class ProvinceController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        query = select(Province)
        result = await self.db.execute(query)
        return result.scalars().all()
