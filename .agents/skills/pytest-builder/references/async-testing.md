# Async Testing with Pytest

FastAPI apps and modern databases (such as Tortoise ORM, Async SQLAlchemy) rely on Python's asynchronous features. Pytest needs specialized plug-ins like `pytest-asyncio` or `anyio` to execute async test functions.

## 1. Setting Up `pytest-asyncio`

Configure `pytest.ini` to auto-discover async tests:

```ini
[pytest]
asyncio_mode = auto
```

Or mark specific tests manually:

```python
import pytest

@pytest.mark.asyncio
async def test_async_operation():
    result = await do_something_async()
    assert result is True
```

## 2. Using `httpx.AsyncClient`

Instead of `fastapi.testclient.TestClient` (which is synchronous), use `httpx.AsyncClient` when testing routes containing long-running operations or middleware dependencies:

```python
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac

@pytest.mark.asyncio
async def test_endpoint(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
```
