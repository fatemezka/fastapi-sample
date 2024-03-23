from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.utils.token_operator import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.api.v1.user.user_controller import UserController
from app.utils.error_handler import ErrorHandler

router = APIRouter()


# token
@router.post("/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
):
    error_list = []
    user_controller = UserController(db)
    user = await user_controller.get_by_username(username=form_data.username)

    # check user authentication
    await user_controller.check_authentication(
        username=form_data.username,
        password=form_data.password,
        error_list=error_list)

    if error_list:
        raise ErrorHandler.bad_request(custom_message={"errors": error_list})

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
