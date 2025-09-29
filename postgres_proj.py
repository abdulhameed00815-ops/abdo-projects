import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="spaine", port=5432)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS person(
    id INT PRIMARY KEY,
    name VARCHAR(255),
    age INT CHECK (age > 0),
    gender CHAR
);
""")

cur.execute("""INSERT INTO person (id, name, age, gender) VALUES
(1, 'mohammed', 65, 'm'),
(2, 'basmalla', 21, 'f'),
(3, 'ronaldo', 43, 'm'),
(4, 'sobhy', 23, 'm');
""")

cur.execute("""CREATE TABLE IF NOT EXISTS boys(
    id SERIAL PRIMARY KEY,
    boy_id INT REFERENCES person(id)
)""")

cur.execute("""INSERT INTO boys (id, boy_id) VALUES
(1, 1)
""")

cur.execute("""SELECT boys.boy_id, person.name, person.age, person.gender
            FROM boys
            JOIN person ON boys.boy_id = person.id;
""")
print(cur.fetchall())


conn.commit()

cur.close()

conn.close()

print("hello")