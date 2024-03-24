from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.error_handler import ErrorHandler
from app.db.base import get_db
from app.schemas import ICreateLawyerBody
from app.api.v1.lawyer.lawyer_controller import LawyerController
from app.api.v1.lawyer.specialty_controller import SpecialtyController
from app.api.v1.user.user_controller import UserController
from app.utils.password_operator import get_password_hash


router = APIRouter()


# register
@router.post("/register")
async def register_route(
        data: ICreateLawyerBody = Body(description="New lawyer fields"),
        db: AsyncSession = Depends(get_db)
):
    error_list = []
    lawyer_controller = LawyerController(db)
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
    user_controller.validate_email_pattern(
        email=data.email, error_list=error_list)

    # check password
    user_controller.validate_password_pattern(
        password=data.password, error_list=error_list)

    # check license_code
    await lawyer_controller.check_license_code_not_exists(license_code=data.licenseCode, error_list=error_list)

    # check specialtyId
    specialty_controller = SpecialtyController(db)
    await specialty_controller.check_specialty_exists(id=data.specialtyId, error_list=error_list)

    if error_list:
        raise ErrorHandler.bad_request(custom_message={"errors": error_list})

    lawyer_items = {
        "isLawyer": True,
        "username": data.username,
        "fullname": data.fullname,
        "phoneNumber": data.phoneNumber,
        "email": data.email,
        "hashedPassword": get_password_hash(data.password),
        "gender": data.gender,
        "age": data.age,
        "maritalStatus": data.maritalStatus,
        "provinceId": data.provinceId,
        "cityId": data.cityId,
        "eduDegree": data.eduDegree,
        "studyField": data.studyField,
        "profilePic": data.profilePic,
        "licenseCode": data.licenseCode,
        "position": data.position,
        "experienceYears": data.experienceYears,
        "biography": data.biography,
        "officePhoneNumber": data.officePhoneNumber,
        "officeAddress": data.officeAddress,
        "specialtyId": data.specialtyId
    }
    lawyer = await lawyer_controller.create(lawyer_items=lawyer_items)
    await db.close()

    return lawyer
