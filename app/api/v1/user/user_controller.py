from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.utils.error_handler import ErrorHandler
from app.models import User
from app.schemas import ICreateUserController, IUpdateUserController
from app.utils.password_operator import verify_password, get_password_hash
import re
import phonenumbers


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

    async def get_by_phone_number(self, phone_number: str):
        user = (await self.db.execute(select(User).where(User.phoneNumber == phone_number))).scalar_one_or_none()
        if not user:  # TODO
            return
        return user

    async def create(self, user_items: ICreateUserController):
        async with self.db as async_session:
            new_user = User(
                isAdmin=False,
                isLawyer=user_items["isLawyer"],
                username=user_items["username"],
                fullname=user_items["fullname"],
                phoneNumber=user_items["phoneNumber"],
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

    async def update_by_id(self, id: int, user_items: IUpdateUserController):
        user = (await self.db.execute(select(User).where(User.id == id))).scalar_one_or_none()
        if user:
            for key, value in user_items.items():
                if value:
                    setattr(user, key, value)
            await self.db.commit()
        return await self.get_by_id(id=id)

    async def update_password_by_id(self, id: int, new_password: str):
        user = await self.get_by_id(id=id)
        if user:
            setattr(user, "hashedPassword", new_password)
            await self.db.commit()
        return await self.get_by_id(id=id)

    # validations

    async def check_authentication(self, username: str, password: str):
        user = await self.get_by_username(username=username)
        if not user:
            raise
        is_valid_password = verify_password(
            plain_password=password, hashed_password=user.hashedPassword)
        if not is_valid_password:
            raise

        return user

    async def verify_current_password(self, id: int, password: str):
        user = await self.get_by_id(id=id)
        is_verified = verify_password(
            plain_password=password, hashed_password=user.hashedPassword)
        if not is_verified:
            raise

    def validate_password_pattern(self, password: str, error_list: list[str] = []):
        # Check length
        if len(password) < 8:
            error_list.append("Password length must be at least 8 characters.")

        # Check for uppercase letters
        if not any(char.isupper() for char in password):
            error_list.append(
                "Password must contain at least one uppercase letter.")

        # Check for lowercase letters
        if not any(char.islower() for char in password):
            error_list.append(
                "Password must contain at least one lowercase letter.")

        # Check for digits
        if not any(char.isdigit() for char in password):
            error_list.append("Password must contain at least one digit.")

        # Check for special characters
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            error_list.append(
                "Password must contain at least one special character.")
        return error_list

    def validate_username_pattern(self, username: str, error_list: list[str] = []):
        # Check length
        if len(username) < 4:
            error_list.append("username length must be at least 4 characters.")

        # Check for uppercase letters
        if any(char.isupper() for char in username):
            error_list.append(
                "UserName must not contain any uppercase letter.")

        # Check for space
        if " " in username:
            error_list.append(
                "Username must not contain space characters.")

        # Check for -
        if "-" in username:
            error_list.append(
                "Username must not contain - characters.")

        # Check for special characters
        if re.search(r'[!#$%^&*(),.?":{}|<>]', username):
            error_list.append(
                "Username must not contain special characters.")
        return error_list

    def validate_phone_number_pattern(self, phone_number: str, error_list: list[str] = []):
        parsed_phone_number = phonenumbers.parse(phone_number)
        is_valid = phonenumbers.is_possible_number(parsed_phone_number)
        if not is_valid:
            error_list.append("Phone number is not valid.")

    def validate_email_pattern(self, email: str, error_list: list[str] = []):
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, email):
            error_list.append("Email is not valid.")

    async def check_username_exists(self, username: str):
        user = (await self.db.execute(select(User).where(User.username == username))).scalar_one_or_none()
        if not user:
            raise ErrorHandler.bad_request(
                "User with this username does not exist.")

    async def check_username_not_exists(self, username: str, error_list: list[str] = []):
        user = (await self.db.execute(select(User).where(User.username == username))).scalar_one_or_none()
        if user:
            error_list.append("User with this username does exist.")

    async def check_phone_number_not_exists(self, phone_number: str, error_list: list[str] = []):
        user = (await self.db.execute(select(User).where(User.phoneNumber == phone_number))).scalar_one_or_none()
        if user:
            error_list.append("User with this phone number does exist.")

    async def check_email_not_exists(self, email: str, error_list: list[str] = []):
        user = (await self.db.execute(select(User).where(User.email == email))).scalar_one_or_none()
        if user:
            error_list.append("User with this email does exist.")

    async def check_username_not_repeat(self, user_id: int, username: str):
        existing_username = (await self.db.execute(select(User).where(User.username == username))).scalar_one_or_none()

        user = (await self.db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()

        if existing_username and existing_username.id != user.id:
            raise ErrorHandler.bad_request(
                custom_message="UserName is repeated.")

    async def check_phone_number_not_repeat(self, user_id: int, phone_number: str):
        existing_phone_number = (await self.db.execute(select(User).where(User.phoneNumber == phone_number))).scalar_one_or_none()

        user = (await self.db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()

        if existing_phone_number and existing_phone_number.id != user.id:
            raise ErrorHandler.bad_request(
                custom_message="Phone number is repeated.")

    async def check_email_not_repeat(self, user_id: int, email: str):
        existing_email = (await self.db.execute(select(User).where(User.email == email))).scalar_one_or_none()

        user = (await self.db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()

        if existing_email and existing_email.id != user.id:
            raise ErrorHandler.bad_request(custom_message="Email is repeated.")
