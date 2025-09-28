import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="spaine", port=5432)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS person(
    id INT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender CHAR
);
""")

cur.execute("""INSERT INTO person (id, name, age, gender) VALUES
(1, 'mohammed', 65, 'm'),
(2, 'basmalla', 21, 'f'),
(3, 'ronaldo', 43, 'm'),
(4, 'sobhy', 23, 'm');
""")

sql = cur.execute("""SELECT * FROM person WHERE starts_with(name, %s) AND age > %s;
""", ("b", 25))

conn.commit()

conn.close()

cur.close()

print("hello")