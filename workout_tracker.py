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
        name1 VARCHAR(255),
        workout_id INT REFERENCES workouts(workouts_id)
);
""")
cur.execute("""INSERT INTO gym_bros (name1, workout_id) VALUES 
        ('jason', 1),
        ('joshua', 2),
        ('jenny', 3);
""")

cur.execute("""ALTER TABLE gym_bros
            ADD CONSTRAINT fk_workout
            FOREIGN KEY (workout_id)
            REFERENCES workouts (workouts_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE;
""")

cur.execute("""CREATE VIEW workouts_done_by_gym_bro AS
            SELECT gym_bros.name1, 
        (SELECT workouts.workout_type FROM workouts WHERE gym_bros.workout_id = workouts.workouts_id)
        FROM gym_bros;
            
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
'c': counts how many workouts of each type exist
'p': total training time per person
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
        cur.execute("""SELECT (*) FROM workouts_done_by_gym_bro
""")
        print(cur.fetchall())
    elif choice == 'c':
        cur.execute("""SELECT workout_type, COUNT(*)
        FROM workouts
        GROUP BY workout_type;
""")
        print(cur.fetchall())
    elif choice == 'p':
        cur.execute("""SELECT gym_bros.name1, SUM(workouts.workout_time) 
        FROM gym_bros
        JOIN workouts ON gym_bros.workout_id = workouts.workouts_id
        GROUP BY gym_bros.name1;
""")
        print(cur.fetchall())
    elif choice == "q":
        break


conn.commit()
cur.close()
conn.close()



























