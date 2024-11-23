import dataclasses
import json

from flask import Flask, request
from datetime import datetime

import task_database

from user_storage import UserData, Role, UserStorage


user_store = UserStorage()
user_store.add_user(UserData(id=1, name='Alice', balance=100, role=Role.PARENT))
user_store.add_user(UserData(id=2, name='Bob', balance=200, role=Role.CHILD))

task_db = task_database.TaskDatabase()

app = Flask(__name__)


@app.route('/my_data', methods=['GET'])
def user_data_endpoint():
    """ Gets all user data of user with given id.
    """
    user_id = int(request.args.get('user_id'))
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    response_dict = {
        'user_id': user.id,
        'name': user.name,
        'balance': user.balance,
        'role': user
    }
    return json.dumps(response_dict)


@app.route('/all_tasks', methods=['GET'])
def all_tasks_endpoint():
    user_id = int(request.args.get('user_id'))
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    tasks = task_db.get_all_tasks()

    response_list = [
        {
            "task_id": t["task_id"],
            "task_name": t["job_name"],
            "reward_amount": t["reward_amount"],
            "created_at": t["created_at"].isoformat(),
            "is_done": t["is_done"],
            "done_by": t["done_by"],
        } for t in tasks
    ]
    return json.dumps(response_list)


@app.route('/active_tasks', methods=['GET'])
def active_tasks_endpoint():
    user_id = int(request.args.get('user_id'))
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    tasks = task_db.get_active_tasks()
    response_list = [
        {
            "task_id": t["task_id"],
            "task_name": t["job_name"],
            "reward_amount": t["reward_amount"],
            "created_at": t["created_at"].isoformat(),
            "is_done": t["is_done"],
            "done_by": t["done_by"],
        } for t in tasks
    ]
    return json.dumps(response_list)


@app.route('/tasks_done_by_me', methods=['GET'])
def tasks_done_by_me_endpoint():
    user_id = int(request.args.get('user_id'))
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    all_tasks = task_db.get_all_tasks()
    done_by_me_tasks = [task for task in all_tasks if task['done_by'] == user_id]

    response_list = [
        {
            "task_id": t["task_id"],
            "task_name": t["job_name"],
            "reward_amount": t["reward_amount"],
            "created_at": t["created_at"].isoformat(),
            "is_done": t["is_done"],
            "done_by": t["done_by"],
        } for t in done_by_me_tasks
    ]
    return json.dumps(response_list)


@app.route('/do_task/<task_id>', methods=['POST'])
def do_task(task_id: str):
    user_id = int(request.args.get('user_id'))
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    task_id_int = int(task_id)
    task = task_db.get_task(task_id_int)

    if task["is_done"]:
        return 'Task already done', 400
    
    task["is_done"] = True
    task["done_by"] = user_id

    task_db.update(task)

    user.balance += task["reward_amount"]
    user_store.update_user(user)

    return 'OK'


if __name__ == '__main__':
    app.run()