from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel('test').save_to_db()
            item = ItemModel('test', 19.99, 1)

            self.assertIsNone(ItemModel.find_by_name('test'),
                              f"Found an item with name {item.name} before save_to_db.")

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'),
                                 f"Did not find an item with name 'test' after save_to_db. Actual: {item.name}")

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'),
                              f"Found an item with name {item.name} after delete_from_db.")
