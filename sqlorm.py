from sqlalchemy import create_engine, Integer, Float, String, Column, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:5432/sqlalchemy_db')

Base = declarative_base

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    things = relationship('Thing', back_populates='Person')

class Thing(Base):
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    value = Column(Integer)
    owner = Column(Integer, ForeignKey('people.id'))
