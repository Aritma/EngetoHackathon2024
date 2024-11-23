import json

from flask import Flask, request

import task_database
import user_storage


user_store = UserStorage()
user_store.add_user(UserData(id=1, name='Alice', balance=100, role=Role.PARENT))
user_store.add_user(UserData(id=2, name='Bob', balance=200, role=Role.CHILD))

app = Flask(__name__)


@app.route('/my_data', methods=['GET'])
def user_data_endpoint(id: str):
    """ Gets all user data of user with given id.
    """
    req = json.loads(request.data)
    user_id = req['user_id']
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    return json.dumps(user)


@app.route('/all_tasks', methods=['GET'])
def task_list():
    req = json.loads(request.data)
    user_id = req['user_id']
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    tasks = task_database.all_tasks()
    return json.dumps(tasks)


@app.route('/all_tasks', methods=['GET'])
def task_list():
    req = json.loads(request.data)
    user_id = req['user_id']
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    tasks = task_database.all_tasks()
    return json.dumps(tasks)


@app.route('/my_tasks', methods=['GET'])
def my_task_list():
    req = json.loads(request.data)
    user_id = req['user_id']
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    tasks = task_database.my_tasks(user_id)
    return json.dumps(tasks)


@app.route('/do_task/<task_id>', methods=['POST'])
def do_task():
    req = json.loads(request.data)
    user_id = req['user_id']
    user = user_store.get_user_by_id(user_id)
    if user is None:
        return 'Unauthorized', 401

    task_id = req['task_id']
    task = task_database.get_task(task_id)

    if task["done"]:
        return 'Task already done', 400
    
    task["done"] = True
    task["done_by"] = user_id

    task_database.update_task(task)

    user.balance += task["reward_amount"]
    user_store.update_user(user)

    return 'Task done'




if __name__ == '__main__':
    app.run()