from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.utils.error_handler import ErrorHandler
from app.models import User
from app.schemas import ICreateUserController
from app.utils.password_operator import verify_password


class UserController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int):
        user = (await self.db.execute(select(User).where(User.id == id))).scalar_one_or_none()
        if not user:  # TODO
            return
        return user

    async def get_by_username(self, username: str):
        user = (await self.db.execute(select(User).where(User.username == username))).scalar_one_or_none()
        if not user:  # TODO
            return
        return user

    async def get_by_email(self, email: str):
        user = (await self.db.execute(select(User).where(User.email == email))).scalar_one_or_none()
        if not user:  # TODO
            return
        return user

    async def create(self, user_items: ICreateUserController):
        async with self.db as async_session:
            new_user = User(
                username=user_items["username"],
                fullname=user_items["fullname"],
                email=user_items["email"],
                hashedPassword=user_items["hashedPassword"]
            )
            async_session.add(new_user)
            await async_session.commit()
            await async_session.refresh(new_user)
            return new_user

    async def delete_by_id(self, id: int):
        user = await self.get_by_id(id=id)

        if user:
            await self.db.execute(delete(User).where(User.id == id))
            await self.db.commit()
        return

    async def check_authentication(self, username: str, password: str):
        user = await self.get_by_username(username=username)
        if not user:
            raise "error"  # TODO
        if not verify_password(plain_password=password, hashed_password=user.hashedPassword):
            raise "error"

        return user
