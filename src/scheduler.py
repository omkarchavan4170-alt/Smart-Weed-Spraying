
# src/scheduler.py

from dataclasses import dataclass
from typing import List


@dataclass
class Task:
    task_id: str
    execution_ms: float
    deadline_ms: float
    arrival_ms: float = 0.0

    def __post_init__(self):
        if self.execution_ms < 0:
            raise ValueError("Execution time cannot be negative.")
        if self.deadline_ms < self.arrival_ms:
            raise ValueError("Deadline cannot precede arrival.")


def edf(tasks: List[Task]) -> List[Task]:
    """Earliest Deadline First, with deterministic tie-breaking."""
    return sorted(
        tasks,
        key=lambda t: (t.deadline_ms, t.arrival_ms, t.task_id)
    )


def simulate_edf(tasks: List[Task]) -> dict:
    """
    Simulate a single, non-preemptive processor using EDF.
    All deadlines are expressed relative to the same time origin.
    """
    pending = list(tasks)
    current_time = 0.0
    schedule = []

    while pending:
        ready = [t for t in pending if t.arrival_ms <= current_time]

        if not ready:
            current_time = min(t.arrival_ms for t in pending)
            ready = [t for t in pending if t.arrival_ms <= current_time]

        task = min(
            ready,
            key=lambda t: (t.deadline_ms, t.arrival_ms, t.task_id)
        )
        pending.remove(task)

        start = max(current_time, task.arrival_ms)
        finish = start + task.execution_ms
        missed = finish > task.deadline_ms

        schedule.append({
            "task_id": task.task_id,
            "arrival_ms": round(task.arrival_ms, 2),
            "start_ms": round(start, 2),
            "execution_ms": round(task.execution_ms, 2),
            "finish_ms": round(finish, 2),
            "deadline_ms": round(task.deadline_ms, 2),
            "deadline_missed": missed,
        })

        current_time = finish

    misses = sum(row["deadline_missed"] for row in schedule)

    return {
        "policy": "EDF",
        "schedule": schedule,
        "total_jobs": len(schedule),
        "deadline_misses": misses,
    }
