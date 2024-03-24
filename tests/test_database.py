from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base, get_db
from app.main import app
import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False},
#     poolclass=StaticPool,
# )
# TestingSessionLocal = sessionmaker(
#     autocommit=False, autoflush=False, bind=engine)

engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False)


class Base(DeclarativeBase):
    pass


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

test_user = {
    "username": "farah",
    "fullname": "farah",
    "phoneNumber": "+989112534343",
    "email": "farah@gmail.com",
    "password": "1234@Farah"
}


def test_register_user():
    response = client.post(
        "/user/register",
        json=test_user,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == test_user["email"]
    assert "id" in data
    user_id = data["id"]


# def test_token_login():
#     user = {"username": test_user["username"],
#             "password": test_user["password"]}
#     response = client.post("/token", data=user)

#     assert response.status_code == 200
#     response = response.json()
#     assert "access_token" in response
#     assert response["token_type"] == "bearer"
