import copy
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Role(str, Enum):
    """Role of a user."""
    PARENT = "parent"
    CHILD = "child"

@dataclass
class UserData:
    """A structure with all user data."""
    id: int
    name: str
    balance: int
    role: Role


class UserStorage:
    """A simple in-memory storage for user data."""
    def __init__(self):
        self.db = {}

    def get_user_by_id(self, user_id: int) -> Optional[UserData]:
        """Gets a user by their ID."""
        user = self.db.get(user_id)
        if user is None:
            return None
        return copy.copy(user)

    def update_user(self, user: UserData) -> None:
        """Updates the user data by the user id."""
        self.db[user.id] = user

    def add_user(self, user: UserData) -> None:
        """Creates a new user in the storage."""
        if self.get_user_by_id(user.id) is not None:
            raise ValueError(f"User with ID {user.id} already exists.")

        self.update_user(user)