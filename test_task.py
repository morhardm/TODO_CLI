import pytest
import json
from pathlib import Path

from todo.task import (
    add_new_task,
    delete_task,
    update_task
)

def load_tasks(p: Path):
    with p.open("r") as f:
        return json.load(f)


def test_add_new_task(tmp_path: pytest.TempPathFactory):
    p = tmp_path / "tasks.json"
    # first add
    add_new_task(str(p), "first")

    tasks = load_tasks(p)
    assert len(tasks) == 1
    assert tasks[0]["id"] == 1
    assert tasks[0]["description"] == "first"

    # second add
    add_new_task(str(p), "second")
    tasks = load_tasks(p)
    assert len(tasks) == 2
    assert {t["id"] for t in tasks} == {1, 2}


def test_delete_task(tmp_path):
    p = tmp_path / "tasks.json"
    # seed two tasks
    with p.open("w") as f:
        json.dump(
            [
                {"id": 1, "description": "a", "status": "todo"},
                {"id": 2, "description": "b", "status": "todo"},
            ],
            f,
            indent=2,
        )

    delete_task(str(p), 1)
    tasks = load_tasks(p)
    assert len(tasks) == 1
    assert tasks[0]["id"] == 2
    assert tasks[0]["description"] == "b"


def test_update_task(tmp_path):
    p = tmp_path / "tasks.json"
    with p.open("w") as f:
        json.dump(
            [{"id": 3,
              "description": "old",
              "status": "todo",
              "created_at": "1999-01-01T00:00:00",
              "updated_at": "2000-01-01T00:00:00"}],
            f,
            indent=2,
        )
    
    update_task(str(p), 3, "new desc")
    tasks = load_tasks(p)
    t = tasks[0]
    assert t["id"] == 3
    assert t["description"] == "new desc"
    assert t["created_at"] != t["updated_at"]



