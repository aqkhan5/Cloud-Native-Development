# Import the pytest testing library for assertion and test running capabilities
import pytest

# Import TestClient from fastapi.testclient. 
# TestClient allows you to make HTTP requests against a FastAPI application without starting a live web server.
from fastapi.testclient import TestClient

# Import the FastAPI application instance ('app') from your main application file (main.py)
from main import app

# Create a client instance by passing the FastAPI 'app' to TestClient.
# This client will be used to simulate HTTP requests (GET, POST, etc.) to the application endpoints.
client = TestClient(app)

# Test function to verify the root endpoint ("/")
def test_root():
    # Simulate a GET request to the root URL "/"
    response = client.get("/")
    
    # Assert that the HTTP response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response body (JSON) matches the expected output {"message": "Hello World"}
    assert response.json() == {"message": "Hello World"}

# Test function to verify the todo list endpoint ("/todo")
def test_todo():
    # Simulate a GET request to the "/todo" URL
    response = client.get("/todo")
    
    # Assert that the HTTP response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response body matches the expected list of todo dictionaries
    assert response.json() == [
        {"id": 1, "task": "Learn FastAPI"}, 
        {"id": 2, "task": "Build a REST API"}
    ]

# Entry point configuration: if this file is run directly (e.g., `python test_main.py`),
# it will execute pytest directly to run the tests defined in this file.
if __name__ == "__main__":
    pytest.main()