# SQLModel and SQLAlchemy Testing

When testing endpoints that communicate with databases, it is crucial to ensure that:
1. Tests run against a clean database instance.
2. Changes made by one test do not affect other tests (Test Isolation).
3. We rollback database transactions automatically upon test completion.

## 1. Setup Transaction-level Isolation

A common pattern with SQLAlchemy is to start a transaction, yield a session, and then roll back the transaction:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a clean SQLite database instance in memory
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

## 2. Using SQLModel

SQLModel works exactly like SQLAlchemy. You can override the DB session using FastAPI's dependency injection system:

```python
from sqlmodel import Session, SQLModel, create_engine
from main import app, get_session

# Override the get_session dependency
@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(scope="function")
def client(session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```
