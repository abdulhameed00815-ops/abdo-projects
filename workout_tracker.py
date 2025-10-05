import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="spaine", port=5432)
cur = conn.cursor()



cur.execute("""CREATE TABLE IF NOT EXISTS workouts(
        workouts_id SERIAL PRIMARY KEY,
        workout_type VARCHAR(255),
        workout_time INT,
        workout_date DATE
    );
""")

cur.execute("""CREATE TABLE IF NOT EXISTS gym_bros(
        name VARCHAR(255),
        workout_id INT
)
""")
cur.execute("""INSERT INTO gym_bros (name, workout_id) VALUES 
        ('jason', 1),
        ('joshua', 2),
        ('jenny', 3);
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
'h': how many times have i done each workout
'g': gym-bro and the workouts he does
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
    elif choice == 'h':
        selected_workout = input("which workout? ")
        cur.execute("""SELECT COUNT(*) FROM workouts WHERE workouts.workout_type = (%s);
""", (selected_workout,))
        print(f"you 've done it {cur.fetchall()} times!")
    elif choice == 'g':
        cur.execute("""SELECT gym_bros.name, 
        (SELECT workouts.workout_type FROM workouts WHERE gym_bros.workout_id = workouts.workouts_id)
        FROM gym_bros;
""")
        print(cur.fetchall())
    elif choice == "q":
        break


conn.commit()
cur.close()
conn.close()



























