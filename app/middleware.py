import os
from fastapi import Request, Depends, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError
from app.utils.token_parser import token_parser
from sqlalchemy.orm import Session
from app.database import get_db
# from app.controllers.user import get_by_id
# from app.controllers.lawyer import get_by_id


class CustomMiddleware(BaseHTTPMiddleware):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={os.getenv("AUTH_HEADER_NAME"): "Bearer"},
    )

    async def dispatch(self, request: Request, call_next, db: Session = Depends(get_db)):
        print("CustomMiddleware applied.")
        if request.url.path.startswith("/specific-api"):
            await self.user_authenticate(request, db)
            print("AUth middleware applied to specific API")

        # Continue processing the request
        response = await call_next(request)
        return response

    async def user_authenticate(self, request: Request, db):
        try:
            user_id = token_parser(request)
            user = await get_user_by_id(db, user_id)
            if not user:
                raise self.credentials_exception
        except:
            print("Request handler error--------------------------")
            raise self.credentials_exception
        print("User Authentication middleware applied")

    async def lawyer_authenticate(self, request: Request, db):
        print("Lawyer Authentication middleware applied")
