import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="spaine", port=5432)
cur = conn.cursor()



cur.execute("""CREATE TABLE IF NOT EXISTS workouts(
        workout_type VARCHAR(255),
        workout_time INT,
        workout_date DATE
    );
""")
conn.commit()

    

def view_workouts():
    cur.execute("""SELECT *
        FROM workouts
""")
    print(cur.fetchall())

while True:
    choice = input("""
's': show workouts
'a': add workout
:
""")
    if choice == "s":
        print(view_workouts())
    elif choice == "a":
        added_workout = input("workout: ")
        cur.execute("""INSERT INTO workouts (workout_type, workout_time, workout_date) VALUES (%s, %s, CURRENT_DATE);
    """, (added_workout, 30))
        print("workout added successfuly!")

cur.close()
conn.close()


























conn.commit()

cur.close()

conn.close()