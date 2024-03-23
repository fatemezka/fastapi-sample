from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.api.v1.user.user_controller import UserController
from app.schemas import ICreateUserBody, ISecureUser, IUpdateUserBody, IUpdateUserPasswordBody
from app.utils.password_operator import get_password_hash
from typing import Annotated
from app.dependencies import get_current_user
from app.utils.error_handler import ErrorHandler

router = APIRouter()
# TODO handle errors list


# register
@router.post("/register", response_model=ISecureUser)
async def register_route(
        data: ICreateUserBody = Body(description="New user fields"),
        db: AsyncSession = Depends(get_db)
):
    error_list = []
    user_controller = UserController(db)

    # check username
    await user_controller.check_username_not_exists(username=data.username, error_list=error_list)
    user_controller.validate_username_pattern(
        username=data.username, error_list=error_list)

    # check phoneNumber
    await user_controller.check_phone_number_not_exists(phone_number=data.phoneNumber, error_list=error_list)
    user_controller.validate_phone_number_pattern(
        phone_number=data.phoneNumber, error_list=error_list)

    # check email
    await user_controller.check_email_not_exists(email=data.email, error_list=error_list)
    # user_controller.validate_email_pattern(
    #     email=data.username, error_list=error_list)  # TODO check

    # check password
    user_controller.validate_password_pattern(
        data.password, error_list=error_list)

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

    if error_list:
        raise ErrorHandler.bad_request(custom_message={"errors": error_list})

    return user


# update
@router.put("/{user_id}")
async def update_route(
    current_user: Annotated[ISecureUser, Depends(get_current_user)],
    user_id: int = Path(description="Id of user to update"),
    data: IUpdateUserBody = Body(..., description="Updated user fields"),
    db: AsyncSession = Depends(get_db)
):
    # check user access
    if user_id != current_user.id:
        raise "do not have access"

    user_controller = UserController(db)

    # check username
    if data.username:
        await user_controller.check_username_not_repeat(user_id, username=data.username)
        user_controller.validate_username_pattern(username=data.username)

    # check phoneNumber
    if data.phoneNumber:
        await user_controller.check_phone_number_not_repeat(user_id, phone_number=data.phoneNumber)
        user_controller.validate_phone_number_pattern(
            phone_number=data.phoneNumber)

    # check email
    if data.email:
        await user_controller.check_email_not_repeat(user_id, email=data.email)
        # user_controller.validate_email_pattern(email=data.email) # TODO check

    user_items = {
        "username": data.username,
        "fullname": data.fullname,
        "phoneNumber": data.phoneNumber,
        "email": data.email
    }
    user = await user_controller.update_by_id(id=user_id, user_items=user_items)
    await db.close()

    return {"message": "User updated successfully"}


# delete
@router.delete("/{user_id}")
async def delete_route(
    current_user: Annotated[ISecureUser, Depends(get_current_user)],
    user_id: int = Path(description="Id of user to delete"),
    db: AsyncSession = Depends(get_db)
):
    # check user access
    if user_id != current_user.id:
        raise ErrorHandler.access_denied("user")

    user_controller = UserController(db)
    await user_controller.delete_by_id(id=user_id)
    await db.close()

    return {"message": "User deleted successfully"}


# change password
@router.put("/change_password/{user_id}")
async def change_password_route(
    current_user: Annotated[ISecureUser, Depends(get_current_user)],
    user_id: int = Path(description="Id of user to change password"),
    data: IUpdateUserPasswordBody = Body(description="Updated user password"),
    db: AsyncSession = Depends(get_db)
):
    # check user access
    if user_id != current_user.id:
        raise "do not have access"

    current_password = data.currentPassword
    new_password = data.newPassword

    user_controller = UserController(db)

    # verify password
    await user_controller.verify_current_password(id=user_id, password=current_password)

    # check password
    user_controller.validate_password_pattern(password=new_password)

    newHashedPassword = get_password_hash(new_password)
    await user_controller.update_password_by_id(id=user_id, new_password=newHashedPassword)
    await db.close()

    return {"message": "User's password changed successfully"}


# get me
@router.get("/me", response_model=ISecureUser)
async def get_me_route(
    current_user: Annotated[ISecureUser, Depends(get_current_user)]
):
    return current_user


# logout
@router.post("/logout")
async def logout_route(
    current_user: Annotated[ISecureUser, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    return {"message": "Logout successfully"}
