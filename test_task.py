import pytest
import datetime
import json
from pathlib import Path

from task import (
    add_new_task
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