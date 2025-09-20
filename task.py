import argparse
import datetime
import json


def main() -> None:
    parser = argparse.ArgumentParser(prog="To-Do CLI", description="To-Do List CLI")
    parser.add_argument("-a", "--add", type=str, help="Add a new task")
    parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")

    args = parser.parse_args()

    if args.add:
        with open('tasks.json', 'r') as f:
            try:
                tasks = json.load(f)
            except FileNotFoundError:
                tasks = []
            except json.JSONDecodeError:
                tasks = []
        # ----- Need to figure out how ^^ works with below -----
        new_task = {'id': 1, #Generate unique ID logic needed
                    'description': args.add,
                    'status': 'todo',
                    'created_at': str(datetime.datetime.now()),
                    'updated_at': str(datetime.datetime.now())
                    }
        with open('tasks.json', 'w') as f:
            json.dump([new_task], f, indent=4)
        
        print("Added New Task!")


if __name__ == "__main__":
    main()