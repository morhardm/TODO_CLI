import argparse
import datetime
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(prog="task", description="To-Do List CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("desc")

    p_update = sub.add_parser("update", help="Update a tasks's description by ID")
    p_update.add_argument("id", type=int)
    p_update.add_argument("desc")

    p_delete = sub.add_parser("delete", help="Delete a task by ID")
    p_delete.add_argument("id", type=int)

    p_mark_in_progress = sub.add_parser("mark-in-progress", help="Mark a task as in progress")
    p_mark_in_progress.add_argument("id", type=int)

    p_mark_done = sub.add_parser("mark-done", help="Mark task as done")
    p_mark_done.add_argument("id", type=int)

    p_list = sub.add_parser("list", help='List tasks (optional status: "todo", "in-progress", "done")')
    p_list.add_argument("status", nargs="?", default="all")

    args = parser.parse_args()

    task_file = 'todo.json'

    if args.cmd == "add":
        add_new_task(file_name=task_file, task_description=args.desc)
    elif args.cmd == "update":
        update_task(file_name=task_file, task_id=args.id, new_desc=args.desc)
    elif args.cmd == "delete":
        delete_task(file_name=task_file, task_id=args.id)
    elif args.cmd == "mark-in-progress":
        mark_in_progress_task(file_name=task_file, task_id=args.id)
    elif args.cmd == "mark-done":
        mark_done_task(file_name=task_file, task_id=args.id)
    elif args.cmd == "list":
        status = None if args.status == "all" else args.status
        list_tasks(task_file, status)


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
            task["updated_at"] = datetime.datetime.now().isoformat()
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
            task["updated_at"] = datetime.datetime.now().isoformat()
            with path.open("w") as f:
                f.write('[\n' + ',\n'.join(json.dumps(t) for t in tasks) + '\n]')
            print(f"Finished Task: {task_id}, status changed to 'done'.")
            return
    
    print(f"No task with ID {task_id} found.")


def list_tasks(file_name: str, status: str | None = None) -> None:
    path = Path(file_name)
    if not path.exists():
        print("No tasks file found.")
        return

    try:
        with path.open("r") as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        print("Tasks file is not valid JSON")
        return
    
    rows = []
    for task in tasks:
        if status is None or task.get("status") == status:
            rows.append([
                task.get("id", ""),
                task.get("description", ""),
                task.get("status", ""),
                task.get("created_at", ""),
                task.get("updated_at", ""),
            ])

    if not rows:
        msg = f"No tasks found for status: {status}." if status else "No tasks found."
        print(msg)
        return
    
    headers = ["ID", "Description", "Status", "Created", "Updated"]
    # column widths
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(str(cell)))

    def fmt(r): return " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(r))

    print(fmt(headers))
    print("-" * (sum(widths) + 3 * (len(widths) - 1)))
    for r in rows:
        print(fmt(r))


if __name__ == "__main__":
    main()