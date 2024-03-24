import pytest
from app.main import app
from httpx import AsyncClient

BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_main():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.get("/")

        assert response.status_code == 404
