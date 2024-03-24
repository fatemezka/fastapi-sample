from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.api.v1.province.province_controller import ProvinceController
from app.utils.error_handler import ErrorHandler


router = APIRouter()


# get all
@router.get("/all")
async def get_all_route(
    db: AsyncSession = Depends(get_db)
):
    province_controller = ProvinceController(db)
    provinces = await province_controller.get_all()
    await db.close()

    return provinces
