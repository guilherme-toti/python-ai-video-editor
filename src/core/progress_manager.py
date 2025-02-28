from typing import Union

from rich.progress import TaskID


class ProgressManager:
    def __init__(self):
        self.progress = None
        self.tasks = {}

    def add_task(self, description: str, total_steps: int) -> Union[None, TaskID]:
        if self.progress is None:
            return None

        task_id = self.progress.add_task(description, total=total_steps)
        self.tasks[task_id] = task_id

        return task_id

    def update_progress(self, task_id: TaskID, step: int) -> None:
        if self.progress is None:
            return None

        self.progress.update(self.tasks[task_id], advance=step)
