
import copy
from dataclasses import dataclass
from enum import Enum
from typing import Optional

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