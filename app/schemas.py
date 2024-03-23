from pydantic import BaseModel
from typing import Optional
# from app.models import MaritalStatus, Sex, LawyerPosition, EducationDegree, RequestType
from enum import Enum


# Token
class Token(BaseModel):
    access_token: str
    token_type: str


class ILoginUser(BaseModel):
    username: str
    password: str


# just for test
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# User
class ISecureUser(BaseModel):
    username: str
    fullname: str
    email: str


class ICreateUserBody(ISecureUser):
    password: str


class ICreateUserController(ISecureUser):
    hashedPassword: str


# class IRegisterUser(BaseModel):
#     username: str
#     name: str
#     family: str
#     phone_number: str
#     password: str
#     email: Optional[str] = None
#     marital_status: Optional[MaritalStatus] = None
#     age: Optional[int] = None
#     sex: Optional[Sex] = None
#     province_id: Optional[int] = None
#     city_id: Optional[int] = None
#     profile_photo: Optional[str] = None


# class IReturnUserInfo(BaseModel):
#     id: int
#     username: str
#     name: str
#     family: str
#     phone_number: str
#     email: Optional[str] = None
#     marital_status: Optional[MaritalStatus] = None
#     age: Optional[int] = None
#     sex: Optional[Sex] = None
#     province_id: Optional[int] = None
#     city_id: Optional[int] = None
#     profile_photo: Optional[str] = None


# # Lawyer
# class IRegisterLawyer(BaseModel):
#     username: str
#     name: str
#     family: str
#     phone_number: str
#     password: str
#     age: int
#     sex: Sex
#     province_id: int
#     city_id: int
#     edu_degree: EducationDegree
#     study_field: str
#     license_code: str
#     position: LawyerPosition
#     experience_years: int
#     biography: str
#     email: Optional[str] = None
#     marital_status: Optional[MaritalStatus] = None
#     profile_photo: Optional[str] = None
#     office_phone_number: Optional[str] = None
#     office_address: Optional[str] = None


# class ILogin(BaseModel):
#     phone_number: str
#     password: str


# # Request
# class ICreateRequest(BaseModel):
#     request_type: RequestType
#     request_subject_id: int
#     description: str
#     lawyer_id: Optional[int] = None
#     attachment_1: Optional[str] = None
#     attachment_2: Optional[str] = None
#     attachment_3: Optional[str] = None


# # Question
# class ICreateQuestion(BaseModel):
#     question_category_id: int
#     description: str
#     is_private: bool
#     lawyer_id: Optional[int] = None


# # Answer
# class ICreateAnswer(BaseModel):
#     lawyer_id: int
#     description: str
