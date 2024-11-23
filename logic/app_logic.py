from persistence.user_storage import UserStorage
from persistence.task_database import TaskDatabase

class BadUserException(Exception):
    pass

class AlreadyDoneException(Exception):
    pass


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
        return self.task_db.get_all_tasks()
    
    def get_active_tasks(self):
        return self.task_db.get_active_tasks()
    
    def get_tasks_done_by_user(self, user_id: int):
        all_tasks = self.task_db.get_all_tasks()
        done_by_user_tasks = [task for task in all_tasks if task['done_by'] == user_id]
        return done_by_user_tasks

    def do_task(self, task_id: int, user_id: int):
        user = self.user_storage.get_user_by_id(user_id)
        if user is None:
            raise BadUserException()

        if user.role == "parent":
            raise RuntimeError("Parent can't do tasks")

        print(task_id)
        task = self.task_db.get_task(task_id)
        if task["is_done"]:
            raise AlreadyDoneException()

        self.task_db.update(task)

        user.balance += task["reward_amount"]
        self.user_storage.update_user(user)

        
