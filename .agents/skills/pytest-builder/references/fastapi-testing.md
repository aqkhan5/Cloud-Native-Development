# FastAPI Testing Reference Guide

Detailed code patterns, mock templates, and database testing configurations for FastAPI using pytest.

## 1. Conftest Configuration (`conftest.py`)

Here is a production-ready `conftest.py` setup implementing client fixtures, async clients, and database session isolation with rollback.

```python
import pytest
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Assuming these are imported from your application
from main import app
from database import Base, get_db

# 1. Isolated Test Database (SQLite in-memory with StaticPool for single connection persistence)
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create database tables once per test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Provide a transactional database session rolled back after each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def override_db(db_session):
    """Override get_db dependency dynamically for every test."""
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()  # Critical clean up!

# 2. Sync TestClient Fixture
@pytest.fixture(scope="function")
def client(override_db) -> Generator[TestClient, None, None]:
    """Synchronous test client with database override pre-configured."""
    with TestClient(app) as c:
        yield c

# 3. AsyncClient Fixture (requires pytest-asyncio or anyio)
@pytest.fixture(scope="function")
async def async_client(override_db) -> AsyncGenerator[AsyncClient, None]:
    """Asynchronous test client with database override pre-configured."""
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac
```

## 2. Advanced Dependency Overrides

FastAPI routes resolve dependencies via `Depends()`. You can override any of these by targeting the original callable.

### Overriding Authentication / JWT Verification

If your routes require authentication, you can mock the authentication dependency directly to return a mock user.

```python
# app/dependencies.py
# def get_current_user(token: str = Depends(oauth2_scheme)): ...

# tests/test_routes.py
from app.dependencies import get_current_user

@pytest.fixture
def mock_admin_user():
    def _mock_admin():
        return {"id": 1, "username": "admin", "role": "admin"}
    
    app.dependency_overrides[get_current_user] = _mock_admin
    yield
    app.dependency_overrides.clear()
```

### Overriding Third-Party APIs (External Calls)

For external APIs (e.g., Stripe, Sendgrid), define a dependency wrapper that performs the API call rather than calling the API directly in the endpoint. Then, override that wrapper in your tests.

```python
# app/services/stripe.py
# class StripeService:
#     def create_charge(self, amount: int): ...
#
# def get_stripe_service() -> StripeService:
#     return StripeService()

# tests/test_payment.py
from app.services.stripe import get_stripe_service

class MockStripeService:
    def create_charge(self, amount: int):
        return {"id": "ch_mock123", "status": "succeeded"}

def test_payment_endpoint(client):
    # Setup override inline for this test
    app.dependency_overrides[get_stripe_service] = lambda: MockStripeService()
    
    try:
        response = client.post("/pay", json={"amount": 1000})
        assert response.status_code == 200
        assert response.json()["status"] == "succeeded"
    finally:
        app.dependency_overrides.clear()
```

## 3. Asynchronous Testing Gotchas

When writing `async def test_...` functions, ensure:
1. You run them with `@pytest.mark.anyio` or `@pytest.mark.asyncio`.
2. Any DB operations performed inside the test code itself are correctly awaited if using an async ORM (like `SQLAlchemy` async extension or `Tortoise-ORM`).
3. You match the signature of the overridden dependency. If the target dependency is an `async def`, the override function must also be `async def`.
