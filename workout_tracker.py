import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="spaine", port=5432)
cur = conn.cursor()



def add_workout():
    cur.execute("""CREATE TABLE IF NOT EXISTS workouts(
        workout_type VARCHAR(255),
        workout_time INT,
        workout_date DATE
    );
""")
    cur.execute("""INSERT INTO workouts (workout_type, workout_time, workout_date) VALUES (%s,%s, CURRENT_DATE)
""", (added_workout, 30))


def view_workouts():
    cur.execute("""SELECT *
        FROM workouts
""")
    print(cur.fetchall())
choice = input(": ")
if choice == "s":
    print(view_workouts())
elif choice == "a":
    add = add_workout()
    print(add)
























conn.commit()

cur.close()

conn.close()