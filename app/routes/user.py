from fastapi import APIRouter, Depends, Path
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.schemas import IRegisterUser, ILoginUser, IReturnUserInfo
from sqlalchemy.orm import Session
from app.utils.error_handler import ErrorHandler
from app.utils.token_operator import token_generator
from app.database import get_db
from app.controllers.user import UserController
from app.utils.password_operator import get_password_hash, verify_password, validate_password_pattern


router = APIRouter()


@router.get("/all")
async def get_users_route(db: Session = Depends(get_db)):
    try:
        user_controller = UserController(db)
        users = user_controller.get_all()
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return users


@router.get("/{id}")
async def get_user_by_id_route(
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of user to return")):
    try:
        user_controller = UserController(db)
        user = user_controller.get_by_id(id)
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    if not user:
        ErrorHandler.not_found("User")

    return user


@router.post("/register")
async def register_user_route(data: IRegisterUser, db: Session = Depends(get_db)):
    user_controller = UserController(db)

    # check phone_number
    user = user_controller.get_by_phone_number(
        data.phone_number)  # TODO check phone_number format
    if user:
        ErrorHandler.bad_request("Phone number does exist")

    # check username
    user = user_controller.get_by_username(data.username)
    if user:
        ErrorHandler.bad_request("Username does exist")

    # check email (if exists)
    if data.email:
        user = user_controller.get_by_email(data.email)
        if user:
            ErrorHandler.bad_request("Email does exist")

    # hash user's password
    if not validate_password_pattern(data.password):
        # frontend should handle that
        return ErrorHandler.bad_request("Password pattern is not valid. [at least 8 characters, contain number, contain upper case, contain lower case, contain special character]")
    try:
        hashed_password = get_password_hash(data.password)

        # create a new user
        user = user_controller.create(
            is_lawyer=False,
            username=data.username,
            name=data.name,
            family=data.family,
            phone_number=data.phone_number,
            hashed_password=hashed_password,
            email=data.email or None,
            marital_status=data.marital_status,
            age=data.age or None,
            sex=data.sex or None,
            province_id=data.province_id or None,
            city_id=data.city_id or None,
            profile_photo=data.profile_photo or None
        )
        user = IReturnUserInfo(
            id=user.id,
            username=user.username,
            name=user.name,
            family=user.family,
            phone_number=user.phone_number,
            email=user.email,
            marital_status=user.marital_status,
            age=user.age,
            sex=user.sex,
            province_id=user.province_id,
            city_id=user.city_id,
            profile_photo=user.profile_photo
        )

        db.close()

        # generate jwt token
        user_token = token_generator(user_id=user.id, is_lawyer=False)
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return {
        "user": user,
        "user_token": user_token
    }


@router.post("/login")
async def login_user_route(data: ILoginUser, db: Session = Depends(get_db)):
    user_controller = UserController(db)
    user = user_controller.get_by_phone_number(data.phone_number)
    if not user:
        ErrorHandler.bad_request("Phone number does not exist")

    is_valid_password = verify_password(data.password, user.hashed_password)
    if not is_valid_password:
        ErrorHandler.bad_request("Password is incorrect")

    try:
        user = IReturnUserInfo(
            id=user.id,
            username=user.username,
            name=user.name,
            family=user.family,
            phone_number=user.phone_number,
            email=user.email,
            marital_status=user.marital_status,
            age=user.age,
            sex=user.sex,
            province_id=user.province_id,
            city_id=user.city_id,
            profile_photo=user.profile_photo
        )
        db.close()

        # generate jwt token
        user_token = token_generator(user_id=user.id, is_lawyer=False)
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return {
        "user": user,
        "user_token": user_token
    }
