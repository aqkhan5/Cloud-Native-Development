import pytest

@pytest.fixture
def temp_user_data():
    """Provides a basic dictionary with user data for tests."""
    return {"username": "testuser", "email": "test@example.com"}
