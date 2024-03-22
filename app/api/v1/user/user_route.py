from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.api.v1.user.user_controller import UserController
from app.schemas import ICreateUserBody, ILoginUser

router = APIRouter()

# TODO add title and description to Body, Query, Path


# get by ID
@router.get("/{user_id}")
async def get_user_by_id_route(
        user_id: int = Path(
            title="User id",
            description="This is ID of user to return"
        ),
        db: AsyncSession = Depends(get_db)
):
    user_controller = UserController(db)
    user = await user_controller.get_by_id(id=user_id)
    await db.close()

    return user


# register
@router.post("/register")
async def register_route(
        data: ICreateUserBody = Body(),
        db: AsyncSession = Depends(get_db)
):
    user_controller = UserController(db)

    # create a new user
    user_items = {
        "username": data.username,
        "fullname": data.fullname,
        "email": data.email,
        "hashedPassword": data.hashedPassword,
    }
    user = await user_controller.create(user_items=user_items)
    await db.close()

    return {
        "user": user
    }


# login
@router.post("/login")
async def login_route(
        data: ILoginUser = Body(),
        db: AsyncSession = Depends(get_db)
):
    user_controller = UserController(db)
    user = await user_controller.get_by_username(username=data.username)
    await db.close()

    return {
        "user": user
    }


# logout
@router.post("/logout")
async def login_route(
        data: ILoginUser = Body(),
        db: AsyncSession = Depends(get_db)
):
    return "Logout successfully"


# delete
@router.delete("/{user_id}")
async def login_route(
        user_id: int = Path(),
        db: AsyncSession = Depends(get_db)
):
    user_controller = UserController(db)
    await user_controller.delete_by_id(id=user_id)
    await db.close()

    return "Deleted successfully"
