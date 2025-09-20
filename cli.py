import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="To-Do List CLI")
    parser.add_argument("-a", "--add", type=str, help="Add a new task")
    tasks = parser.parse_args()
    
    print("Added Task:", tasks.add)


if __name__ == "__main__":
    main()