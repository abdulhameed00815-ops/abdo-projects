from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, func

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/sqlalchemy_db", echo=True)

meta = MetaData()

people = Table(
    "people",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("age", Integer),
)


things = Table(
    "things",
    meta,
    Column('id', Integer, primary_key=True),
    Column('description', String, nullable=False),
    Column('owner', Integer, ForeignKey('people.id')),
    Column('value', Integer)

)

meta.create_all(engine)

conn = engine.connect()

insert_people = people.insert().values([
    {"name": "ben", "age": 18},
    {"name": "joe", "age": 55},
    {"name": "fred", "age": 33},
    {"name": "basmallah", "age": 21}
])
conn.execute(insert_people)
conn.commit()

insert_things = things.insert().values([
    {"description": "cup", "value": 20, "owner": 1},
    {"description": "ball", "value": 400, "owner": 2},
    {"description": "toothbrush", "value": 51, "owner": 3},
    {"description": "lipstick", "value": 250, "owner": 4},
])
conn.execute(insert_things)
conn.commit()

group_by_statement = things.select().with_only_columns(things.c.owner, func.sum(things.c.value)).group_by(things.c.owner)

result = conn.execute(group_by_statement)

for row in result.fetchall():
    print(row)

