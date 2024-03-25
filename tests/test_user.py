import pytest
from app.main import app
from httpx import AsyncClient

BASE_URL = "http://localhost:8000"

test_user = {
    "username": "farah",
    "fullname": "farah",
    "phoneNumber": "+989112534343",
    "email": "farah@gmail.com",
    "password": "1234@Farah"
}


@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/user/register", json=test_user)

    assert response.status_code == 200
    response = response.json()
    assert response["username"] == test_user["username"]


@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        login_user = {
            "username": test_user["username"], "password": test_user["password"]}
        response = await client.post("/token", data=login_user, follow_redirects=True)

    # assert response == "SAMPLE TEXT"
    assert response.status_code == 200
    response = response.json()
    assert "access_token" in response
    assert response["token_type"] == "bearer"
