# todo-cli

A **Task Tracker CLI** that stores tasks in a JSON file and gives you commands like:  
task add "Buy milk"  
task update 1 "Buy oat milk"  
task list  
task list todo  
task start 2  
task finish 2  
task delete 3  

---

## Install

### Recommended method: pipx (good for CLI tools)
```bash
python -m pip install --user pipx
pipx ensurepath
pipx install git+https://github.com/<morhardm>/todo-cli.git
```
After install, the task command should be on your PATH.

---

## Usage
``` bash
# Add
task add "Walk the dog"

# Update description
task update 1 "Walk the dog (park at 6pm)"

# Start / Finish
task start 1
task finish 1

# List (all or by status)
task list
task list todo
task list in-progress
task list done

# Delete
task delete 1
```
---

## Where data is stored

By default, the CLI reads/writes todo.json in your current working directory.
Run task in different folders to keep separate lists per project.

#### JSON format:
```json
[
  {
    "id": 1,
    "description": "Walk the dog",
    "status": "todo",
    "created_at": "2025-09-21T13:00:00.000000",
    "updated_at": "2025-09-21T13:00:00.000000"
  }
]
```