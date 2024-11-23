from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from persistence.user_storage import UserStorage
from persistence.task_database import TaskDatabase

class BadUserException(Exception):
    pass

class AlreadyDoneException(Exception):
    pass

class TaskStatus(str, Enum):
    ACTIVE = "active"
    PAID = "paid"
    WAITING = "waiting"

@dataclass
class Task:
    id: int
    task_name: str
    description: str 
    reward_amount: int
    difficulty_level: str
    created_at: datetime 
    is_done: bool
    done_by: int
    done_at: datetime
    waiting: bool

    @classmethod
    def load_from_dict(cls, data: dict):
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
        if not self.is_done:
            return TaskStatus.ACTIVE
        if self.waiting:
            return TaskStatus.WAITING
        else:
            return TaskStatus.PAID


class AppLogic:
    def __init__(self, user_storage: UserStorage, task_db: TaskDatabase):
        self.user_storage = user_storage
        self.task_db = task_db

    def get_user_data(self, user_id: int):
        user = self.user_storage.get_user_by_id(user_id)
        if user is None:
            raise BadUserException()

        return user

    def get_all_tasks(self):
        return [Task.load_from_dict(t) for t in self.task_db.get_all_tasks()]
    
    def get_active_tasks(self):
        return [Task.load_from_dict(t) for t in self.task_db.get_active_tasks()]
    
    def get_tasks_done_by_user(self, user_id: int):
        all_tasks = [Task.load_from_dict(t) for t in self.task_db.get_all_tasks()]
        done_by_user_tasks = [task for task in all_tasks if task.done_by == user_id]
        return done_by_user_tasks

    def do_task(self, task_id: int, user_id: int, pay_now: bool):
        user = self.user_storage.get_user_by_id(user_id)
        if user is None:
            raise BadUserException()

        if user.role == "parent":
            raise RuntimeError("Parent can't do tasks")

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
