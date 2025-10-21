from sqlalchemy import create_engine, Integer, Float, String, Column, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

Base = declarative_base()

DATABASE_URL = "postgresql+asyncpg://postgres:your_password@localhost/api_db"

engine = create_async_engine(DATABASE_URL, echo=True)

Async_Session_Local = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    async with Async_Session_Local() as session:
        yield session

