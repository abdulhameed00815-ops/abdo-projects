from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/sqlalchemy_db", echo=True)

meta = MetaData()

people = Table(
    "people",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("age", Integer, ForeignKey('people.id')),
)


things = Table(
    "things",
    meta,
    Column('id', Integer, primary_key=True),
    Column('description', String, nullable=False),
    Column('owner', Integer),
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

conn.commit()

insert_things = things.insert().values([
    {"description": "cup", "value": 20, "owner": 1},
    {"description": "ball", "value": 400, "owner": 2},
    {"description": "toothbrush", "value": 51, "owner": 3},
    {"description": "lipstick", "value": 250, "owner": 4},
])

conn.commit()

join_statement = people.join(things, people.c.id == things.c.owner)
select_statement = people.select().with_only_columns(people.c.name, things.c.description).select_from(join_statement)
result = conn.execute(select_statement)

for row in result.fetchall():
    print(row)

