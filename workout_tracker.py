import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="spaine", port=5432)
cur = conn.cursor()



cur.execute("""CREATE TABLE IF NOT EXISTS workouts(
        workout_type VARCHAR(255),
        workout_time INT,
        workout_date DATE
    );
""")


def add_workout():
    added_workout = input("workout: ")
    cur.execute("""INSERT INTO workouts (workout_type, workout_time, workout_date) VALUES (%s, %s, CURRENT_DATE);
        """, (added_workout, 30))
    print("workout added successfuly!")

def weekly_workouts():
    cur.execute("""SELECT * FROM workouts WHERE workout_date >= CURRENT_DATE - INTERVAL '7 days';
""")
    print(cur.fetchall())

def time_trained():
    cur.execute("""SELECT SUM(workouts.workout_time) AS total_time FROM workouts;
""")
    print(cur.fetchall())

while True:
    choice = input("""
's': show all-time workouts
'a': add workout
'q': quit
'w': show week workouts
't': show all-time time spent training (seconds)
:
""")
    if choice == "s":
        cur.execute("SELECT * FROM workouts;")
        print(cur.fetchall())
    elif choice == "a":
        add_workout()
    elif choice == "w":
        weekly_workouts()
    elif choice == 't':
        time_trained()
    elif choice == "q":
        break


conn.commit()
cur.close()
conn.close()



























