import json
from datetime import datetime
import os

expenses_file = "expenses.json"

def load_expenses():
    if not os.path.exists(expenses_file):
        return {"expenses": []}
    with open(expenses_file, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"expenses": []}

def save_expenses(data):
    with open(expenses_file, "w") as f:
        json.dump(data, f, indent=4)

expenses = load_expenses()

print("yeah this is the update")

print("branch1")
while True:
    usr_options = input("""

    click '+' to add a new expense,
    click '-' to remove a expense,
    click 'q' to quit :),
    click 'u' to update an expense,
    click 's' to show all expenses,
    click 't' to show total spent of all time,
    click 'm' to show total spent of all month
                               :""")
    usr_options = usr_options.lower()

    if usr_options == '+':
        if usr_options == '+':
            expense_description = input("New expense: ")
            expense_amount = float(input("Amount: "))
            expense_date = datetime.now()
            date_string = expense_date.strftime("%d/%m/%Y")

            new_expense = {
                "description": expense_description,
                "amount": expense_amount,
                "date": date_string
            }

            expenses["expenses"].append(new_expense)
            save_expenses(expenses)
            print("Expense added!")
    elif usr_options == 's':
        for expense in expenses["expenses"]:
            print(f"{expense['description']}-{expense['amount']}egp {expense['date']}")
    elif usr_options == 't':
            total = sum(expense["amount"] for expense in expenses["expenses"])
            print(f"total: {total}")
    elif usr_options == 'm':
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        monthly_total = sum(
            expense["amount"]
            for expense in expenses["expenses"]
            if datetime.strptime(expense["date"], "%d/%m/%Y").month == current_month
            and datetime.strptime(expense["date"], "%d/%m/%Y").year == current_year
        )
        print(f"monthly total: {monthly_total}")
    elif usr_options == '-':
        for expense in expenses["expenses"]:
            print(f"{expense['description']}")
        unwanted_expense = input("which one to remove? (enter task number): ")
        for expense in expenses["expenses"]:
            if expense["description"] == unwanted_expense:
                expenses["expenses"].remove(expense)  # remove that task object
                save_expenses(expenses)
                print("expense removed!")
    elif usr_options == 'u':
        for expense in expenses["expenses"]:
            print(f"{expense['description']}")
            expense_to_update = input("which one to update? (enter expense description): ")
            update = input("Enter new description: ")
            if expense["description"] == expense_to_update:
                expense["description"] = update
                save_expenses(expenses)
                print("expense updated!")



