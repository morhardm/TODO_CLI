import argparse
import datetime
import json
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(prog="To-Do CLI", description="To-Do List CLI")
    parser.add_argument("-a", "--add", type=str, help="Add a new task")
    parser.add_argument("-u", "--update", nargs=2, metavar=("ID", "DESC"), help="Update a task's description by ID")
    parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
    parser.add_argument("-s", "--start", type=int, help="Marks a task as 'in progress'")
    parser.add_argument("-f", "--finish", type=int, help="Marks a task as 'done'")
    # List argument (lists all, lists all done, lists all in progress)


    args = parser.parse_args()

    task_file = 'tasks.json'

    if args.add:
        try:
            add_new_task(file_name=task_file, task_description=args.add)
        except UnboundLocalError:
            sys.exit("Add Task")
    
    if args.update:
        task_id_str, new_desc = args.update
        task_id = int(task_id_str)
        update_task(file_name=task_file, task_id=task_id, new_desc=new_desc)

    if args.delete:
        delete_task(file_name=task_file, task_id=args.delete)

    if args.start:
        mark_in_progress_task(file_name=task_file, task_id=args.start)
    
    if args.finish:
        mark_done_task(file_name=task_file, task_id=args.finish)


def add_new_task(file_name: str, task_description: str) -> None:
    """
    Creates New Tasks and adds them to tasks.json, creates the file if it does not yet exist
    """
    now = datetime.datetime.now().isoformat()
    new_task = {
        'id': None,  # to be set later
        'description': task_description,
        'status': 'todo',
        'created_at': now,
        'updated_at': now,
    }
    path = Path(f"{file_name}")
    if path.exists():
        with path.open("r") as f:
            tasks = json.load(f) # expects the file to contain a JSON list
    else:
        tasks = []
    # ID Logic
    max_id = max((task.get('id', 0) for task in tasks), default=0)
    new_task['id'] = max_id + 1
    # Always append newest task to list (if empty or not)
    tasks.append(new_task)

    # Rewrites entire file every time
    with path.open("w") as f:
        f.write('[\n' + ',\n'.join(json.dumps(t) for t in tasks) + '\n]')
    
    print(f"Added new task! Task ID: {new_task['id']}")


def update_task(file_name: str, task_id: int, new_desc: str) -> None:
    """
    Updates description of existing tasks, select by ID
    """
    path = Path(file_name)
    if not path.exists():
        print("No tasks file found.")
        return
    
    try:
        with path.open("r") as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        print("Tasks file is not valid JSON.")
        return
    
    for task in tasks:
        if task.get("id") == task_id:
            task["description"] = new_desc
            task["updated_at"] = datetime.datetime.now().isoformat()
            with path.open("w") as f:
                f.write('[\n' + ',\n'.join(json.dumps(t) for t in tasks) + '\n]')
            print(f"Updated task {task_id}.")
            return
    
    print(f"No task with ID {task_id} found.")


def delete_task(file_name: str, task_id: int) -> None:
    """
    Deletes Tasks in tasks.json, select by ID
    """
    path = Path(file_name)
    if not path.exists():
        print("No tasks file found.")
        return
    
    # Load tasks (handle empty/corrupt JSON)
    try:
        with path.open("r") as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        tasks = []

    before = len(tasks)
    tasks = [task for task in tasks if task.get("id") != task_id]

    if len(tasks) == before:
        print(f"No task with ID {task_id} found.")

    with path.open("w") as f:
        f.write('[\n' + ',\n'.join(json.dumps(t) for t in tasks) + '\n]')
    
    print(f"Deleted task {task_id}.")


def mark_in_progress_task(file_name: str, task_id: int) -> None:
    """
    Updates status of task to "in-progress"
    """
    path = Path(file_name)
    if not path.exists():
        print("No tasks file found.")
        return
    
    try:
        with path.open("r") as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        print("Tasks file is not valid JSON.")
        return
    
    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = "in-progress"
            with path.open("w") as f:
                f.write('[\n' + ',\n'.join(json.dumps(t) for t in tasks) + '\n]')
            print(f"Updated task {task_id} to in-progress.")
            return
    
    print(f"No task with ID {task_id} found.")

def mark_done_task(file_name: str, task_id: int) -> None:
    """
    Updates status of task to "done"
    """
    path = Path(file_name)
    if not path.exists():
        print("No tasks file found.")
        return
    
    try:
        with path.open("r") as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        print("Tasks file is not valid JSON.")
        return
    
    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = "done"
            with path.open("w") as f:
                f.write('[\n' + ',\n'.join(json.dumps(t) for t in tasks) + '\n]')
            print(f"Finished Task: {task_id}, status changed to 'done'.")
            return
    
    print(f"No task with ID {task_id} found.")


if __name__ == "__main__":
    main()