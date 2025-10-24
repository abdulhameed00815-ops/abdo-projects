from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from enum import IntEnum
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Todo as TodoModel, Priority
api = FastAPI()
from sqlalchemy import create_engine, Integer, Float, String, Column, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import asyncio

Base = declarative_base()

DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost/api_db"

engine = create_async_engine(DATABASE_URL, echo=True)

Async_Session_Local = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with Async_Session_Local() as session:
        yield session

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description='name of the todo')
    priority: Priority = Field(default=Priority.LOW, description='priority of todo')

class TodoCreate(TodoBase):
    pass

class TodoModel(TodoBase):
    todo_id: int = Field(..., description='unique identifier for todo')

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description='name of the todo')
    priority: Optional[Priority] = Field(None, description='priority of todo')




@api.get('/todos/{todo_id}', response_model=TodoModel)
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TodoModel).where(TodoModel.todo_id == todo_id))
    todo = result.scalar_one_or_none()
    if todo is None:
       raise HTTPException(status_code=404, detail='todo not found bitch!')
    return todo

@api.get('/todos', response_model=List[TodoModel])
async def get_todos(first_n: int | None=None, db: AsyncSession = Depends(get_db)):
    query = select(TodoModel)
    if first_n:
        query = query.limit(first_n)
    result = await db.execute(query)
    Todos = result.scalars().all()
    return Todos


@api.post('/todos', response_model=TodoModel)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    new_todo = TodoModel(
        todo_name=todo.todo_name,
        priority=todo.priority
    )
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    return new_todo


@api.put('/todo/{todo_id}', response_model=TodoModel)
async def update_todo(todo_id: int, updated_todo: TodoUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TodoModel).where(TodoModel.todo_id == todo_id))
    todo = result.scalars().first()

    if not todo:
        raise HTTPException(status_code=404, detail='todo not found bitch!')
    todo.todo_name == updated_todo.todo_name
    todo.priority == updated_todo.priority
    await db.commit()
    await db.refresh(todo)
    return todo

@api.delete('/todo/{todo_id}', response_model=TodoModel)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TodoModel).where(TodoModel.todo_id == todo_id))
    todo = result.scalars().first()
    if not todo:
        raise HTTPException(status_code=404, detail='todo not found bitch!')
    await db.delete(todo)
    await db.commit()
    return {"message": "TodoModel deleted successfully"}

