# from httpx import AsyncClient
# from app.main import app

# BASE_URL = "http://localhost:8000"


# @pytest.mark.asyncio
# async def test_login_user():
#     async with AsyncClient(app=app, base_url=BASE_URL) as client:
#         user = {"username": "fateme", "password": "1234@Fateme"}
#         response = await client.post("/token", data=user)

#         assert response.status_code == 200
#         assert "access_token" in response.json()

from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)


# @pytest.mark.asyncio
def test_token_login():
    user = {"username": "fateme", "password": "1234@Fateme"}
    response = client.post("/token", data=user)

    assert response.status_code == 200
    response = response.json()
    assert "access_token" in response
    assert response["token_type"] == "bearer"


def test_register_user():
    user = {
        "username": "farah",
        "fullname": "farah",
        "phoneNumber": "+989112334343",
        "email": "farah@gmail.com",
        "password": "1234@Farah"
    }
    response = client.post("/user/register", json=user)

    assert response.status_code == 200
    response = response.json()
    assert response["username"] == "farah"
