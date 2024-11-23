import json
import functools

from enum import Enum

from flask import Flask, request, jsonify
from flask_cors import CORS

from logic.app_logic import AppLogic
from persistence.user_storage import UserData, Role, UserStorage
from persistence.task_database import TaskDatabaseSQL


def validate_request(f):
  @functools.wraps(f)
  def decorated_function(*args, **kwargs):
    user_id = request.args.get('user_id', type=int)
    if user_id is None:
        return 'Bad Request - Missing params', 400

    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401
    return f(user, *args, **kwargs)
  return decorated_function

user_store = UserStorage()
user_store.add_user(UserData(id=1, name='Alice', balance=100, role=Role.PARENT))
user_store.add_user(UserData(id=2, name='Bob', balance=200, role=Role.CHILD))

task_db = TaskDatabaseSQL()

logic = AppLogic(user_storage=user_store, task_db=task_db)


app = Flask(__name__)
CORS(app)


def format_task_for_response(task: dict) -> dict:
    return {
        "task_id": task.id,
        "task_name": task.task_name,
        "reward_amount": task.reward_amount,
        "created_at": task.created_at.isoformat(),
        "is_done": task.is_done,
        "done_by": task.done_by,
        "status": task.status(),
    }


def str_to_bool(s: str) -> bool:
    return s.lower() == "true"

@app.route('/my_data', methods=['GET'])
@validate_request
def user_data_endpoint(user):
    """ Gets all user data of user with given id.
    """
    response_dict = {
        'user_id': user.id,
        'name': user.name,
        'balance': user.balance,
        'role': user.role,
    }
    return jsonify(response_dict)


@app.route('/all_tasks', methods=['GET'])
@validate_request
def all_tasks_endpoint(*args,**kwargs):
    tasks = logic.get_all_tasks()
    response_list = [
        format_task_for_response(t) for t in tasks
    ]

    return jsonify(response_list)


@app.route('/active_tasks', methods=['GET'])
@validate_request
def active_tasks_endpoint(*args,**kwargs):
    tasks = logic.get_active_tasks()
    response_list = [
        format_task_for_response(t) for t in tasks
    ]
    return jsonify(response_list)


@app.route('/tasks_done_by_me', methods=['GET'])
@validate_request
def tasks_done_by_me_endpoint(user):
    done_by_me_tasks = logic.get_tasks_done_by_user(user.id)

    response_list = [
        format_task_for_response(t) for t in done_by_me_tasks
    ]
    return jsonify(response_list)


@app.route('/do_task/<task_id>', methods=['POST'])
@validate_request
def do_task(user, task_id: str):
    pay_now_str = request.args.get('pay_now')
    pay_now = str_to_bool(pay_now_str)

    task_id_int = int(task_id)
    logic.do_task(task_id_int, user.id, pay_now=pay_now)

    result = {
        "status": "OK"
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run()