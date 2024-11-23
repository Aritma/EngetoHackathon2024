"""This module contains the application business logic. It is separate
from the presentation layer (Flask) and the data storage layer
to allow for easy testing.

The data storage classes are provided using the dependency injection pattern.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from persistence.user_storage import UserStorage
from persistence.task_database import TaskDatabase

class BadUserException(Exception):
    """Raised when an invalid user id is provided."""
    pass

class AlreadyDoneException(Exception):
    """Raised when attempting to complete a task that is already done."""
    pass

class ParentCantDoTasksException(Exception):
    """Raised when a parent tries to complete a task."""
    pass

class TaskStatus(str, Enum):
    """Status of a single task.
    
    ACTIVE: The task is available for completion.
    PAID: The task has been completed and immediately paid for.
    WAITING: The task has been completed, but selected for delayed payment.
    """
    ACTIVE = "active"
    PAID = "paid"
    WAITING = "waiting"

@dataclass
class Task:
    """Represents a single task."""
    id: int
    task_name: str
    description: str 
    reward_amount: int
    difficulty_level: str
    created_at: datetime 
    is_done: bool
    done_by: Optional[int]  # user_id of the user who completed the task
    done_at: datetime
    waiting: bool

    @classmethod
    def load_from_dict(cls, data: dict):
        """Loads a task from representation on the persistance layer."""
        return cls(
            id=data["task_id"],
            task_name=data["job_name"],
            description=data["description"],
            reward_amount=data["reward_amount"],
            difficulty_level=data["difficulty_level"],
            created_at=data["created_at"],
            is_done=data["is_done"],
            done_by=data["done_by"],
            done_at=data["done_at"],
            waiting=data["waiting"]
        )

    def status(self) -> TaskStatus:
        """Computes the comletion status of the task."""
        if not self.is_done:
            return TaskStatus.ACTIVE
        if self.waiting:
            return TaskStatus.WAITING
        else:
            return TaskStatus.PAID


class AppLogic:
    """Business logic of the application.
    
    For now, this is simple enough to be contained in a single class.
    Persistence-layer entities are passed in the constructor (dependency injection).
    """
    def __init__(self, user_storage: UserStorage, task_db: TaskDatabase):
        self.user_storage = user_storage
        self.task_db = task_db

    def get_user_data(self, user_id: int):
        """Gets the user information of a user with given id."""
        user = self.user_storage.get_user_by_id(user_id)
        if user is None:
            raise BadUserException()

        return user

    def get_all_tasks(self):
        """Gets the list of all tasks."""
        return [Task.load_from_dict(t) for t in self.task_db.get_all_tasks()]
    
    def get_active_tasks(self):
        """Gets the list of all active tasks (available to be completed)."""
        return [Task.load_from_dict(t) for t in self.task_db.get_active_tasks()]
    
    def get_tasks_done_by_user(self, user_id: int):
        """Gets the list of all tasks completed by a user with given id."""
        all_tasks = [Task.load_from_dict(t) for t in self.task_db.get_all_tasks()]
        done_by_user_tasks = [task for task in all_tasks if task.done_by == user_id]
        return done_by_user_tasks

    def do_task(self, task_id: int, user_id: int, pay_now: bool):
        """Processes task completion of a task with given id by user with given id."""
        user = self.user_storage.get_user_by_id(user_id)
        if user is None:
            raise BadUserException()

        if user.role == "parent":
            raise ParentCantDoTasksException()

        # Get the task, modify and store it back
        task = self.task_db.get_task(task_id)
        if task["is_done"]:
            raise AlreadyDoneException()

        task["is_done"] = True
        task["done_by"] = user_id
        task["waiting"] = not pay_now

        self.task_db.update(task)

        if pay_now:
            user.balance += task["reward_amount"]
        self.user_storage.update_user(user)
