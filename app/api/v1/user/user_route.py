from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.api.v1.user.user_controller import UserController
from app.schemas import ICreateUserBody, ISecureUser
from app.utils.password_operator import get_password_hash
from typing import Annotated
from app.dependencies import get_current_user

router = APIRouter()

# TODO add title and description to Body, Query, Path


# get by ID
@router.get("/me", response_model=ISecureUser)
async def get_me_route(
    current_user: Annotated[ISecureUser, Depends(get_current_user)]
):
    return current_user


# register
@router.post("/register", response_model=ISecureUser)
async def register_route(
        data: ICreateUserBody = Body(description="New user fields"),
        db: AsyncSession = Depends(get_db)
):
    user_controller = UserController(db)

    # check username
    await user_controller.check_username_not_exists(data.userName)
    user_controller.validate_username_pattern(data.userName)

    # check email
    await user_controller.check_email_not_exists(data.email)
    user_controller.validate_email_pattern(data.userName)

    # check password
    user_controller.validate_password_pattern(data.password)

    user_items = {
        "isLawyer": False,
        "username": data.username,
        "fullname": data.fullname,
        "phoneNumber": data.phoneNumber,
        "email": data.email,
        "hashedPassword": get_password_hash(password=data.password)
    }
    user = await user_controller.create(user_items=user_items)
    await db.close()

    # TODO handle errors list
    return user


# logout
@router.post("/logout")
async def login_route(
        db: AsyncSession = Depends(get_db)
):
    return "Logout successfully"


# delete
@router.delete("/{user_id}")
async def login_route(
    current_user: Annotated[ISecureUser, Depends(get_current_user)],
    user_id: int = Path(description="Id of user to delete"),
    db: AsyncSession = Depends(get_db)
):
    user_controller = UserController(db)

    if user_id != current_user.id:
        raise "do not have access"

    await user_controller.delete_by_id(id=user_id)
    await db.close()

    return "Deleted successfully"
