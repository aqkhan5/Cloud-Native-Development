# fastapi-hello world
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
def delete_todo(item_id:int):
    """Delete a todo by its ID"""
    return{"message": f"Todo_item with ID {item_id} deleted."}

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
    