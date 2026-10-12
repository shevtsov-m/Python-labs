tasks = {
    "Homework": "completed",
    "Clean room": "in progress",
    "Buy groceries": "pending",
    "Learn Python": "pending"
}

def add_task(name, status):
    if name not in tasks:
        tasks[name] = status

def remove_task(name):
    del tasks[name]

def change_status(name, status):
    if name in tasks:
        tasks[name] = status

add_task("Go for a walk with dog", "pending")
change_status("Clean room", "completed")
remove_task("Homework")

pending_tasks = []

for name in tasks:
    if tasks[name] == "pending":
        pending_tasks.append(name)

print("All the task are: ", tasks)
print("Tasks with status pending are: ", pending_tasks)