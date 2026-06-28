from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

todos = []
next_id = 1


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False
    created_at: datetime = None


@app.get("/todos")
def list_todos():
    return todos


@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate):
    global next_id
    new_todo = Todo(id=next_id, title=todo.title, created_at=datetime.now())
    todos.append(new_todo)
    next_id += 1
    return new_todo


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for t in todos:
        if t.id == todo_id:
            return t
    raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, data: TodoUpdate):
    for t in todos:
        if t.id == todo_id:
            if data.title is not None:
                t.title = data.title
            if data.completed is not None:
                t.completed = data.completed
            return t
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    for i, t in enumerate(todos):
        if t.id == todo_id:
            todos.pop(i)
            return
    raise HTTPException(status_code=404, detail="Todo not found")
