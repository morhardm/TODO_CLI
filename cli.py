import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="To-Do List CLI")
    parser.add_argument("-task", type=str, help="Task description")
    args = parser.parse_args()
    
    print("args.task:", args.task)

if __name__ == "__main__":
    main()