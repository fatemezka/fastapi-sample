import os
from fastapi import Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.api.v1.user.user_controller import UserController
from app.utils.error_handler import ErrorHandler


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise ErrorHandler.user_unauthorized(
                message="Could not validate credentials")

    except JWTError:
        raise ErrorHandler.user_unauthorized(message="Token is not valid.")

    user_controller = UserController(db)
    user = await user_controller.get_by_id(id=user_id)

    if user is None:
        raise ErrorHandler.user_unauthorized(message="Token is not valid.")

    return user
