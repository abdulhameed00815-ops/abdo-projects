from sqlalchemy import create_engine, Integer, Float, String, Column, ForeignKey, func, Enum
from enum import IntEnum
from sqlalchemy import create_engine, Integer, Float, String, Column, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

Base = declarative_base()

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1


class Todo(Base):
    __tablename__ = 'todos'
    
    todo_id = Column(Integer, primary_key=True, index=True)
    todo_name = Column(String(512), nullable=False)
    priority = Column(Enum(Priority), default=Priority.LOW)