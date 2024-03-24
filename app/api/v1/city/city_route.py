from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.api.v1.city.city_controller import CityController
from app.utils.error_handler import ErrorHandler


router = APIRouter()


# get all
@router.get("/all")
async def get_all_route(
    province_id: int = Query(
        description="ID of the province to retrieve its cities."),
    db: AsyncSession = Depends(get_db)
):
    city_controller = CityController(db)
    cities = await city_controller.get_all(province_id)
    await db.close()

    return cities
