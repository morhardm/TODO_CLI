'''
Requirements:
User Should be able to:
1. Add, Update, and Delete Tasks
2. Mark a task as in progress or done
3. List all tasks
4. List all tasks that are done
5. List all tasks that are not done
6. List all tasks that are in progress

Constraints:
1. Use positional arguments in command line to accept user inputs
2. Use a JSON file to store the tasks in the current directory
3. The JSON file should be created if it does not exist
4. Use the native file system module of your programming language to interact with the JSON file
5. Do not use any external libraries or frameworks to build this project
6. Ensure to handle errors and edge cases gracefully

Example Commands:
# Adding a new task
task-cli add "Buy groceries"
# Output: Task added successfully (ID: 1)
# Updating and deleting tasks
task-cli update 1 "Buy groceries and cook dinner"
task-cli delete 1
# Marking a task as in progress or done
task-cli mark-in-progress 1
task-cli mark-done 1
# Listing all tasks
task-cli list
# Listing tasks by status
task-cli list done
task-cli list todo
task-cli list in-progress


Task Properties:
- ID: Unique identifier for each task
- Description: Text description of the task
- Status: Can be "todo", "in-progress", or "done"
- created_at: Timestamp when the task was created
- updated_at: Timestamp when the task was last updated

Make sure to add these properties to the JSON file when adding a new task and update them when updating a task.
'''

print("Hello To-Do List!")