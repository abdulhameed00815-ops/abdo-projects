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

cur.execute("""SELECT COUNT(*) FROM workouts
""")


workouts_count = cur.fetchone()[0]
if workouts_count == 0:
    cur.execute("""INSERT INTO workouts (workout_type, workout_time, workout_date) VALUES
        ('pushups', 30, CURRENT_DATE),
        ('jumping jacks', 30, CURRENT_DATE),
        ('squats', 30, CURRENT_DATE);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS gym_bros(
        gym_bro_id SERIAL PRIMARY KEY,
        name1 VARCHAR(255),
        workout_id INT
);
""")

cur.execute("SELECT COUNT(*) FROM gym_bros;")
count = cur.fetchone()[0]
if count == 0:
    cur.execute("""INSERT INTO gym_bros (name1, workout_id) VALUES 
            ('jason', 1),
            ('joshua', 2),
            ('jenny', 3);
    """)

#i encountered an error where everytime i rerun the code the interpreter  tries to recreate the existing constraint on the gym bros table, so i added this line to start fresh everytime i rerun the code
cur.execute("""
    ALTER TABLE gym_bros
    DROP CONSTRAINT IF EXISTS fk_workout;
""")

cur.execute("""ALTER TABLE gym_bros
            ADD CONSTRAINT fk_workout
            FOREIGN KEY (workout_id)
            REFERENCES workouts (workouts_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE;
""")
conn.commit()

#just a view set as a function instead of making a whole new table or defining a function
cur.execute("""CREATE OR REPLACE VIEW workouts_done_by_gym_bro AS
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
'u': update workout
'd': delete workout
'x': how many gymbros have done the workout
:
""").lower()
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
        cur.execute("""SELECT *
                    FROM workouts_done_by_gym_bro
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
    elif choice == 'u':
        cur.execute("SELECT * FROM workouts;")
        print(cur.fetchall())
        workout_to_update = input("which workout to update? (enter id)")
        new_workout = input("new workout: ")
        cur.execute("""UPDATE workouts
                    SET workout_type = (%s)
                    WHERE workouts_id = (%s);
""", (new_workout, workout_to_update))
        print("workout updated successfuly!")
    elif choice == 'd':
        cur.execute("SELECT * FROM workouts;")
        print(cur.fetchall())
        workout_to_delete = input("which workout to delete? (enter id)")
        cur.execute("""DELETE FROM workouts
                    WHERE workouts_id = (%s);
""", (workout_to_delete))
        conn.commit()

        print("workout updated deleted!")
    elif choice == "x":
        cur.execute("""WITH workouts_count AS (
            SELECT workout_id, COUNT(*) AS count_per_workout
            FROM gym_bros
            GROUP BY workout_id
            )
            SELECT workouts.workout_type, workouts_count.count_per_workout
            FROM workouts
            JOIN workouts_count ON workouts.workouts_id = workouts_count.workout_id;
""")
        print(cur.fetchall())
    elif choice == "q":
        break


conn.commit()
cur.close()
conn.close()



























