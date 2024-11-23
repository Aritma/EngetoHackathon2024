import json
from dataclasses import dataclass
from enum import Enum

from flask import Flask, request

class Role(Enum):
    PARENT = 1
    CHILD = 2

@dataclass
class UserData:
    id: int
    name: str
    balance: int
    role: Role

class UserStorage:
    def __init__(self):
        self.db = {}

    def get_user_by_id(self, user_id: int) -> UserData:
        return self.db.get(user_id).copy()

    def update_user(self, user: UserData) -> None:
        self.db[user.id] = user

    def add_user(self, user: UserData) -> None:
        self.db[user.id] = user


user_store = UserStorage()
user_store.add_user(UserData(id=1, name='Alice', balance=100, role=Role.PARENT))
user_store.add_user(UserData(id=2, name='Bob', balance=200, role=Role.CHILD))

app = Flask(__name__)

@app.route('/dummy', methods=['PUT'])
def dummy():
    # For now, let's copy this to every request
    req = json.loads(request.data)
    user_id = req['user_id']
    user = user_store.get_user_by_id(user_id)

if __name__ == '__main__':
    app.run()