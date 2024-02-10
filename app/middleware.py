from fastapi import Request, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError
from app.utils.token_operator import token_parser
from sqlalchemy.orm import Session
from app.database import get_db


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next, db: Session = Depends(get_db)):
        print("CustomMiddleware applied.")
        if request.url.path.startswith("/specific-api"):
            await self.user_authenticate(request, db)
            print("AUth middleware applied to specific API")

        # Continue processing the request
        response = await call_next(request)
        return response

    async def user_authenticate(self, request: Request, db):
        # try:
        #     user_id = token_parser(request)
        #     user = await get_user_by_id(db, user_id)
        #     if not user:
        #         raise self.credentials_exception
        # except:
        #     raise self.credentials_exception
        print("User Authentication middleware applied")

    async def lawyer_authenticate(self, request: Request, db):
        print("Lawyer Authentication middleware applied")
