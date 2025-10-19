from fastapi import FastAPI
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
    

all_todos = [
    {'todo_id': 1, 'todo_name': 'clean'},
    {'todo_id': 2, 'todo_name': 'workout'},
    {'todo_id': 3, 'todo_name': 'study'},
    {'todo_id': 4, 'todo_name': 'chill'}
]

@api.get('/')
def index():
    return {'message': 'hello world'}

@api.get('/todos/{todo_id}')
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return {'result': todo}

@api.get('/todos')
def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos


@api.post('/todos')
def create_todo(todo: dict):
    new_todo_id = max(todo["todo.id"] for todo in all_todos) + 1
    new_todo = {
        'todo_id': new_todo_id,
        'todo_name': todo["todo.name"]
    }

    all_todos.append(new_todo)
    return new_todo