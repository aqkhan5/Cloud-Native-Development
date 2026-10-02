import pytest
from typing import Generator
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

# TODO: Replace 'main' and 'app' with your actual FastAPI instance import
# from main import app

@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """Provides a synchronous FastAPI TestClient."""
    # Assuming 'app' is your FastAPI instance
    # with TestClient(app) as c:
    #     yield c
    pass

@pytest.fixture(scope="function")
async def async_client() -> Generator[AsyncClient, None, None]:
    """Provides an asynchronous TestClient using HTTPX."""
    # async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
    #     yield ac
    pass
