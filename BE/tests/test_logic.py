from unittest import TestCase
from logic.app_logic import Task
from datetime import datetime

time = datetime.now()
task = Task(id=99,
            task_name='test',
            description='test',
            reward_amount=99,
            difficulty_level='test',
            created_at=time,
            is_done=True,
            done_by=1,
            done_at=time,
            waiting=False)


class TestAppLogic(TestCase):

    def test_task_should_be_initiatible(self):
        self.assertIsInstance(task, Task)
