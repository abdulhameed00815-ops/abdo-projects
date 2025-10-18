from fastapi import FastAPI
api = FastAPI()

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