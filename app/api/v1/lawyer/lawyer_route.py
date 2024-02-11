from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.utils.error_handler import ErrorHandler
from app.utils.token_operator import token_generator
from app.database import get_db
from app.schemas import IRegisterLawyer, ILogin
from app.api.v1.lawyer.lawyer_controller import LawyerController
from app.api.v1.user.user_controller import UserController
from app.utils.password_operator import get_password_hash, verify_password, validate_password_pattern


router = APIRouter()


@router.get("/all")
async def get_lawyers_route(db: Session = Depends(get_db)):
    try:
        lawyer_controller = LawyerController(db)
        lawyers = lawyer_controller.get_all()
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return lawyers


@router.get("/{id}")
async def get_lawyer_by_id_route(
        db: Session = Depends(get_db),
        id: int = Path(description="This is ID of lawyer to return")):
    try:
        lawyer_controller = LawyerController(db)
        lawyer = lawyer_controller.get_by_id(id)
        db.close()
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    if not lawyer:
        ErrorHandler.not_found("Lawyer")
    return lawyer


@router.post("/register")
async def register_lawyer_route(data: IRegisterLawyer, db: Session = Depends(get_db)):
    lawyer_controller = LawyerController(db)
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

    # check license_code
    lawyer = lawyer_controller.get_by_license_code(data.license_code)
    if lawyer:
        ErrorHandler.bad_request("This license code does exists!")

    # hash user's password
    if not validate_password_pattern(data.password):
        return ErrorHandler.bad_request("Password pattern is not valid. [at least 8 characters, contain number, contain upper case, contain lower case, contain special character]")
    try:
        hashed_password = get_password_hash(data.password)

        # create user and then lawyer
        result = lawyer_controller.create_user_and_lawyer(
            username=data.username,
            name=data.name,
            family=data.family,
            phone_number=data.phone_number,
            hashed_password=hashed_password,
            age=data.age,
            sex=data.sex,
            province_id=data.province_id,
            city_id=data.city_id,
            edu_degree=data.edu_degree,
            study_field=data.study_field,
            license_code=data.license_code,
            position=data.position,
            experience_years=data.experience_years,
            biography=data.biography,
            email=data.email or None,
            marital_status=data.marital_status or None,
            profile_photo=data.profile_photo or None,
            office_phone_number=data.office_phone_number or None,
            office_address=data.office_address or None
        )
        db.close()

        print("Result:", result)
        # generate jwt token
        user = result["user"]
        lawyer = result["lawyer"]
        lawyer_token = token_generator(
            user_id=user.id, lawyer_id=lawyer.id, is_lawyer=True)
    except Exception as e:
        ErrorHandler.internal_server_error(e)

    return {
        "user": user,
        "lawyer": lawyer,
        "lawyer_token": lawyer_token
    }
