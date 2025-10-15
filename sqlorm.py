from sqlalchemy import create_engine, Integer, Float, String, Column, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:5432/sqlalchemy_db')

Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    things = relationship('Thing', back_populates='person')

class Thing(Base):
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    value = Column(Integer)
    owner = Column(Integer, ForeignKey('people.id'))
    person = relationship('Person', back_populates='things')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_person = Person(name='esra2', age=17)
session.add(new_person)
session.flush()

new_thing = Thing(description='robe', value=1400, owner=new_person.id)
session.add(new_thing)
session.commit()

result = session.query(Thing.owner, func.sum(Thing.value)).group_by(Thing.owner).all()

print(result)