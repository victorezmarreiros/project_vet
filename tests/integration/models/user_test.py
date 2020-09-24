from tests.base_test import BaseTest
from models.user import UserModel


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', 'test123')

            self.assertIsNone(user.find_by_username('test'),
                              f"Found a user with name {user.username!r} before save_to_db.")
            self.assertIsNone(user.find_by_id(1),
                              f"Found a user with id {user.id} before save_to_db.")

            user.save_to_db()

            self.assertIsNotNone(user.find_by_username('test'),
                                 f"Did not find an user with name {user.username!r} after save_to_db.")
            self.assertIsNotNone(user.find_by_id(1),
                                 f"Did not find an user with id {user.id} after save_to_db.")
