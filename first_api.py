from fastapi import FastAPI, HTTPException
from typing import List, Optional
from enum import IntEnum
from pydantic import BaseModel, Field
api = FastAPI()

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description='name of the todo')
    priority: Priority = Field(default=Priority.LOW, description='priority of todo')

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description='unique identifier for todo')

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description='name of the todo')
    priority: Optional[Priority] = Field(None, description='priority of todo')

all_todos = [
        Todo(todo_id=1, todo_name='code'),
        Todo(todo_id=2, todo_name='clean'),
        Todo(todo_id=3, todo_name='workout')
]


@api.get('/todos/{todo_id}', response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    
    raise HTTPException(status_code=404, detail='todo not found bitch!')

@api.get('/todos', response_model=List[Todo])
def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos


@api.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    new_todo = Todo(todo_id=new_todo_id, todo_name=todo.todo_name, priority=todo.priority)


    all_todos.append(new_todo)
    return new_todo

@api.put('/todo/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, updated_todo=TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            todo.todo_name == update_todo.todo_name
            todo.priority == update_todo.priority
            return todo
    raise HTTPException(status_code=404, detail='todo not found bitch!')

@api.delete('/todo/{todo_id}', response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            delete_todo = all_todos.pop(index)
            return delete_todo
    raise HTTPException(status_code=404, detail='todo not found bitch!')

