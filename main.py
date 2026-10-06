# fastapi-hello world
import os
import sys
from contextlib import asynccontextmanager
from urllib.parse import urlparse, urlunparse

from fastapi import FastAPI
from pydantic import BaseModel


def mask_database_url(url: str) -> str:
    """Mask user credentials/passwords in database connection URLs."""
    try:
        parsed = urlparse(url)
        if parsed.password:
            netloc = f"{parsed.username}:****@{parsed.hostname}"
            if parsed.port:
                netloc += f":{parsed.port}"
            return urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))
        elif "@" in url:
            parts = url.split("@")
            prefix = parts[0]
            host_part = "@".join(parts[1:])
            if ":" in prefix:
                scheme_user = prefix.split(":")[:-1]
                return f"{':'.join(scheme_user)}:****@{host_part}"
            return f"****@{host_part}"
        return url
    except Exception:
        return "****"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler for FastAPI startup and shutdown."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("CRITICAL ERROR: DATABASE_URL environment variable is missing!", file=sys.stderr)
        os._exit(1)
    
    print(f"Connected to: {mask_database_url(database_url)}")
    yield


app = FastAPI(lifespan=lifespan)


class TodoItem(BaseModel):
    id: int
    task: str
    time_estimate: int = None  # Optional field with a default value of None


class TodoItemResponse(BaseModel):
    id: int
    task: str
    time_estimate: int = None  # Optional field with a default value of None
    completed: bool = False  # Optional field with a default value of False


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/todo")
def todo():
    my_todo = [{"id": 1, "task": "Learn FastAPI"}, {"id": 2, "task": "Build a REST API"}]
    return my_todo


@app.post("/todo")
def create_todo(todo: TodoItem) -> TodoItemResponse:
    # Create a new TodoItemResponse object based on the input TodoItem
    todo_response = TodoItemResponse(**todo.dict(), completed=False)
    return todo_response


@app.delete("/todo/{item_id}")
def delete_todo(item_id: int):
    """Delete a todo by its ID"""
    return {"message": f"Todo_item with ID {item_id} deleted."}


@app.put("/todo/{item_id}")
def update_todo(item_id: int, todo: TodoItem) -> TodoItemResponse:
    # Create a new TodoItemResponse object based on the input TodoItem and the provided item_id
    todo_response = TodoItemResponse(id=item_id, **todo.dict(), completed=False)
    return todo_response


@app.patch("/todo/{item_id}")
def partial_update_todo(item_id: int, todo: TodoItem) -> TodoItemResponse:
    # Create a new TodoItemResponse object based on the input TodoItem and the provided item_id
    todo_response = TodoItemResponse(id=item_id, task="Sample Task", completed=False)
    return todo_response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)