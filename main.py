from datetime import datetime
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from schemas import Todo, TodoCreate, TodoUpdate

app = FastAPI()

todos: list[Todo] = []


def _find_todo(todo_id: UUID) -> Todo | None:
    for t in todos:
        if t.id == todo_id:
            return t
    return None


@app.exception_handler(HTTPException)
def http_exception_handler(_request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/todos")
def list_todos():
    """Tüm todo'ları listeler."""
    return todos


@app.post("/todos", status_code=201)
def create_todo(data: TodoCreate):
    """Yeni bir todo ekler."""
    todo = Todo(id=uuid4(), title=data.title, created_at=datetime.now())
    todos.append(todo)
    return todo


@app.get("/todos/{todo_id}")
def get_todo(todo_id: UUID):
    """ID'ye göre tek bir todo getirir."""
    todo = _find_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}")
def update_todo(todo_id: UUID, data: TodoUpdate):
    """Todo başlık veya tamamlanma durumunu günceller."""
    todo = _find_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    if data.title is not None:
        todo.title = data.title
    if data.completed is not None:
        todo.completed = data.completed
    return todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: UUID):
    """ID'ye göre todo siler."""
    for i, t in enumerate(todos):
        if t.id == todo_id:
            todos.pop(i)
            return
    raise HTTPException(status_code=404, detail="Todo not found")
