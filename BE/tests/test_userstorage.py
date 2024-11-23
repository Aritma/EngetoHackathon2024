from unittest import TestCase
from persistence.user_storage import UserData, Role

class TestUserStorage(TestCase):

    def test_userdata_should_be_initiatible(self):
        self.assertIsInstance(UserData(1,'test',balance=100,role=Role.CHILD),UserData)
