import pytest
from app.main import app
from httpx import AsyncClient

BASE_URL = "http://localhost:8000"

test_lawyer = {
    "gender": "female",
    "age": 40,
    "maritalStatus": "Single",
    "provinceId": 1,
    "cityId": 1,
    "eduDegree": "Bachelor",
    "studyField": "Law",
    "profilePic": None,
    "licenseCode": "12fer",
    "position": "Lawyer",
    "experienceYears": 0,
    "biography": "sample bio",
    "officePhoneNumber": "",
    "officeAddress": "",
    "specialtyId": 2,
    "username": "sepide",
    "fullname": "sepide",
    "phoneNumber": "+989123339900",
    "email": "sepide@gmail.com",
    "password": "1234@Sepide"
}


@pytest.mark.asyncio
async def test_register_lawyer():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/lawyer/register", json=test_lawyer)

        assert response.status_code == 200
        response = response.json()
        assert response["licenseCode"] == test_lawyer["licenseCode"]
        assert response["provinceId"] == test_lawyer["provinceId"]


@pytest.mark.asyncio
async def test_get_all_lawyers():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.get("/lawyer/all")

        assert response.status_code == 200
        response = response.json()
        assert type(response) == list
        assert len(response) >= 1
