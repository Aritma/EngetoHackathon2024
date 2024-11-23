import json

from enum import Enum

from flask import Flask, request, jsonify
from flask_cors import CORS

from logic.app_logic import AppLogic
from persistence.user_storage import UserData, Role, UserStorage
from persistence.task_database import TaskDatabase


user_store = UserStorage()
user_store.add_user(UserData(id=1, name='Alice', balance=100, role=Role.PARENT))
user_store.add_user(UserData(id=2, name='Bob', balance=200, role=Role.CHILD))

task_db = TaskDatabase()

logic = AppLogic(user_storage=user_store, task_db=task_db)

class TaskStatus(str, Enum):
    ACTIVE = "active"
    PAID = "paid"
    WAITING = "waiting"

app = Flask(__name__)
CORS(app)


def format_task_for_response(task: dict) -> dict:
    return {
        "task_id": task["task_id"],
        "task_name": task["job_name"],
        "reward_amount": task["reward_amount"],
        "created_at": task["created_at"].isoformat(),
        "is_done": task["is_done"],
        "done_by": task["done_by"],
        "status": (
            TaskStatus.ACTIVE.value if not task["is_done"]
            else TaskStatus.WAITING if task["waiting"]
            else TaskStatus.PAID.value
        )
    }


def str_to_bool(s: str) -> bool:
    return s.lower() == "true"


@app.route('/my_data', methods=['GET'])
def user_data_endpoint():
    """ Gets all user data of user with given id.
    """
    user_id = int(request.args.get('user_id'))
    user = logic.get_user_data(user_id)

    response_dict = {
        'user_id': user.id,
        'name': user.name,
        'balance': user.balance,
        'role': user.role,
    }
    return jsonify(response_dict)


@app.route('/all_tasks', methods=['GET'])
def all_tasks_endpoint():
    user_id = int(request.args.get('user_id'))
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    tasks = logic.get_all_tasks()
    response_list = [
        format_task_for_response(t) for t in tasks
    ]

    return jsonify(response_list)


@app.route('/active_tasks', methods=['GET'])
def active_tasks_endpoint():
    user_id = int(request.args.get('user_id'))
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    tasks = logic.get_active_tasks()
    response_list = [
        format_task_for_response(t) for t in tasks
    ]
    return jsonify(response_list)


@app.route('/tasks_done_by_me', methods=['GET'])
def tasks_done_by_me_endpoint():
    user_id = int(request.args.get('user_id'))
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    done_by_me_tasks = logic.get_tasks_done_by_user(user_id)

    response_list = [
        format_task_for_response(t) for t in done_by_me_tasks
    ]
    return jsonify(response_list)


@app.route('/do_task/<task_id>', methods=['POST'])
def do_task(task_id: str):
    pay_now_str = request.args.get('pay_now')
    pay_now = str_to_bool(pay_now_str)

    user_id = int(request.args.get('user_id'))
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    task_id_int = int(task_id)
    logic.do_task(task_id_int, user_id, pay_now=pay_now)

    result = {
        "status": "OK"
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run()