import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return {"tasks": []}  # start with empty list
    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"tasks": []}  # fallback if file is corrupted


def save_tasks(data):
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Add a new task ---
tasks = load_tasks()


# pick the next id based on the max id, not just length
if tasks["tasks"]:
    next_id = max(task["id"] for task in tasks["tasks"]) + 1
else:
    next_id = 1

task_status = ""
for task in tasks["tasks"]:
    if task["completed"] == True:
        task_status = "(completed)"
    elif task["completed"] == False:
        task_status = "(not completed)"


while True:
    usr_options = input("""
    
click '+' to add a new task,
click '-' to remove a task,
click 'q' to quit :),
click 'f' to finish a task,
click 'u' to update a task,
click 's' to show all tasks 
                           :""")
    usr_options = usr_options.lower()

    if usr_options == '+':
        task_description = input("new task: ")
        new_task = {
            "id": next_id,
            "description": task_description,
            "completed": False
        }

        print(new_task)
        tasks["tasks"].append(new_task)
        save_tasks(tasks)
        print("Task added!")
    elif usr_options == 's':
        for task in tasks["tasks"]:
            task_status = '(completed)' if task["completed"] else '(not completed)'
            print(f"{task["id"]}: {task['description']} {task_status}")
    elif usr_options == '-':
        for task in tasks["tasks"]:
            print(f"{task["id"]}: {task['description']}")
        unwanted_task = input("which one to remove? (enter task number): ")
        for task in tasks["tasks"]:
            if task["id"] == int(unwanted_task):
                tasks["tasks"].remove(task)  # remove that task object
                save_tasks(tasks)
                print("Task removed!")
    elif usr_options == 'f':
        for task in tasks["tasks"]:
            task_status = '(completed)' if task["completed"] else '(not completed)'
            print(f"{task["id"]}: {task['description']} {task_status}")
        finished_task = input("which one did you finish? (enter task number): ")
        for task in tasks["tasks"]:
            if task["id"] == int(finished_task):
                task["completed"] = True
                save_tasks(tasks)
                print("Task set to completed!")
    elif usr_options == "u":
        for task in tasks["tasks"]:
            task_status = '(completed)' if task["completed"] else '(not completed)'
            print(f"{task["id"]}: {task['description']} {task_status}")
        task_to_update = input("which one to update? (enter task number): ")
        update = input("Enter new description: ")
        for task in tasks["tasks"]:
            if task["id"] == int(task_to_update):
                task["description"] = update
                save_tasks(tasks)
                print("Task updated!")
    elif usr_options == 'q':
        break



