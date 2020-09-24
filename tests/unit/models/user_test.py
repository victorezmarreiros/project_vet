from tests.unit.unit_base_test import UnitBaseTest
from models.user import UserModel


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test', 'test123')
        self.assertEqual(user.username, 'test',
                         "The username of the user after de creation does not equal to the constructor argument.")
        self.assertEqual(user.password, 'test123',
                         "The password of the user after de creation does not equal to the constructor argument.")

