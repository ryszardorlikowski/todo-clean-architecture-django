import uuid
from dataclasses import dataclass
from datetime import datetime

from boards.domain.value_objects import TaskId, BoardId

BOARD_TASKS_LIMIT: int = 20


class BoardExceededTasksLimit(Exception):
    """"""


class NotUniqueTaskTitleInBoard(Exception):
    """"""


class TaskIsAlreadyDone(Exception):
    """"""


@dataclass
class Task:
    id: TaskId
    title: str
    created: datetime
    done: bool = False

    @property
    def is_done(self):
        return self.done

    def complete_task(self):
        if self.done:
            raise TaskIsAlreadyDone
        self.done = True


@dataclass
class Board:
    id: BoardId
    title: str
    tasks: list[Task]

    def add_new_task(self, title: str) -> None:
        if self.number_of_tasks == BOARD_TASKS_LIMIT:
            raise BoardExceededTasksLimit

        if not self.__check_title_is_unique(title):
            raise NotUniqueTaskTitleInBoard

        new_task = Task(
            id=uuid.uuid4(),
            title=title,
            created=datetime.now()
        )
        self.tasks.append(new_task)

    @property
    def number_of_tasks(self) -> int:
        return len(self.tasks)

    def __check_title_is_unique(self, title):
        return all([not task.title == title for task in self.tasks])

    def remove_task(self, task_id: TaskId):
        self.tasks = list(filter(lambda task: task.id != task_id, self.tasks))