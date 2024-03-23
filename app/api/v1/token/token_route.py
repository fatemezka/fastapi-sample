from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.utils.token_operator import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.api.v1.user.user_controller import UserController

router = APIRouter()


# token
@router.post("/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
):

    user_controller = UserController(db)
    user = await user_controller.get_by_username(username=form_data.username)

    # TODO error handler
    # check user authentication
    await user_controller.check_authentication(
        username=form_data.username,
        password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


# # sample auth api
# @router.get("/users/me/", response_model=ISecureUser)
# async def read_users_me(
#     current_user: Annotated[ISecureUser, Depends(get_current_user)]
# ):
#     return current_user
