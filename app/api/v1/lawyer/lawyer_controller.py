from sqlalchemy.orm import Session
from app.models import Lawyer, User
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.utils.error_handler import ErrorHandler
from app.schemas import ICreateLawyerController


class LawyerController:
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self, province_id: int | None = None, city_id: int | None = None, specialty_id: int | None = None):
        query = select(Lawyer).options(
            joinedload(Lawyer.user).defer(User.hashedPassword).defer(User.isAdmin)).options(
            joinedload(Lawyer.specialty)).options(
            joinedload(Lawyer.province)).options(
            joinedload(Lawyer.city))

        if province_id:
            query = query.filter(Lawyer.provinceId == province_id)
        if city_id:
            query = query.filter(Lawyer.cityId == city_id)
        if specialty_id:
            query = query.filter(Lawyer.specialtyId == specialty_id)

        result = await self.db.execute(query)
        lawyers = result.scalars().all()
        return lawyers

    async def get_by_id(self, id: int):
        query = select(Lawyer).options(
            joinedload(Lawyer.user).defer(User.hashedPassword).defer(User.isAdmin)).options(
            joinedload(Lawyer.specialty)).options(
            joinedload(Lawyer.province)).options(
            joinedload(Lawyer.city)).where(Lawyer.id == id)

        result = await self.db.execute(query)
        lawyer = result.scalar_one_or_none()
        if not lawyer:
            raise ErrorHandler.not_found("Lawyer")
        return lawyer

    async def create(self, lawyer_items: ICreateLawyerController):
        async with self.db as async_session:
            new_user = User(
                isAdmin=False,
                isLawyer=lawyer_items["isLawyer"],
                username=lawyer_items["username"],
                fullname=lawyer_items["fullname"],
                phoneNumber=lawyer_items["phoneNumber"],
                email=lawyer_items["email"],
                hashedPassword=lawyer_items["hashedPassword"]
            )
            async_session.add(new_user)
            await async_session.commit()
            await async_session.refresh(new_user)

            print(new_user)
            new_lawyer = Lawyer(
                userId=new_user.id,
                gender=lawyer_items["gender"],
                age=lawyer_items["age"],
                maritalStatus=lawyer_items["maritalStatus"],
                provinceId=lawyer_items["provinceId"],
                cityId=lawyer_items["cityId"],
                eduDegree=lawyer_items["eduDegree"],
                studyField=lawyer_items["studyField"],
                profilePic=lawyer_items["profilePic"],
                licenseCode=lawyer_items["licenseCode"],
                position=lawyer_items["position"],
                experienceYears=lawyer_items["experienceYears"],
                biography=lawyer_items["biography"],
                officePhoneNumber=lawyer_items["officePhoneNumber"],
                officeAddress=lawyer_items["officeAddress"],
                specialtyId=lawyer_items["specialtyId"]
            )
            async_session.add(new_lawyer)
            await async_session.commit()
            await async_session.refresh(new_lawyer)

            return new_lawyer

    # validations
    async def check_license_code_not_exists(self, license_code: str, error_list: list[str] = []):
        lawyer = (await self.db.execute(select(Lawyer).where(Lawyer.licenseCode == license_code))).scalar_one_or_none()
        if lawyer:
            error_list.append("License code does exist.")
