from unittest import TestCase
from user_storage import UserData, Role

class TestDummy(TestCase):

    def test_userdata_should_be_initiatible(self):
        self.assertIsInstance(UserData(1,'test',balance=100,role=Role.CHILD),UserData)
