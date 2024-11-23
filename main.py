import copy
import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flask import Flask, request

class Role(str, Enum):
    PARENT = "parent"
    CHILD = "child"

@dataclass
class UserData:
    id: int
    name: str
    balance: int
    role: Role

class UserStorage:
    def __init__(self):
        self.db = {}

    def get_user_by_id(self, user_id: int) -> Optional[UserData]:
        user = self.db.get(user_id)
        if user is None:
            return None
        return copy.copy(user)

    def update_user(self, user: UserData) -> None:
        self.db[user.id] = user

    def add_user(self, user: UserData) -> None:
        self.db[user.id] = user


user_store = UserStorage()
user_store.add_user(UserData(id=1, name='Alice', balance=100, role=Role.PARENT))
user_store.add_user(UserData(id=2, name='Bob', balance=200, role=Role.CHILD))

app = Flask(__name__)

@app.route('/user_data/<id>', methods=['GET'])
def user_data_endpoint(id: str):
    id = int(id)
    user = user_store.get_user_by_id(id)
    if user is None:
        return 'User not found', 404

    return json.dumps(user.__dict__)

@app.route('/dummy', methods=['PUT'])
def dummy():
    # For now, let's copy this to every request
    req = json.loads(request.data)
    user_id = req['user_id']
    user = user_store.get_user_by_id(user_id)

if __name__ == '__main__':
    app.run()