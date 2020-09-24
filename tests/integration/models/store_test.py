from models.item import ItemModel
from tests.base_test import BaseTest

from models.store import StoreModel


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('Test')
        self.assertEqual(store.items.all(), [ ],
                         f"The stores's items length was not 0 even though no items were added.")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('Test Store')

            self.assertIsNone(StoreModel.find_by_name('Test Store'),
                              "Found a store with a name 'Test Store' before save_to_db.")

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('Test Store'),
                                 "Did not find a store with name 'Test Store' after save_to_db.")

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('Test Store'),
                              "Found a store after delete_from_db with name 'Test Store'")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('Test Store')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1,
                             "The count of the items after save_to_db does not equal to 1")

            self.assertEqual(store.items.first().name, 'test_item',
                             "The name of the first item after save_to_db does not equal to 'test_item' as expected.")

    def test_store_json(self):
        store = StoreModel('Store Test')
        expected = {
            'id': None,
            'name': 'Store Test',
            'items': []
        }
        self.assertDictEqual(expected, store.json(),
                             f"The JSON export of the store is incorrect. Received {store.json()}, expected {expected}.")

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('Test Store')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'id': 1,
                'name': 'Test Store',
                'items': [{'name': 'test_item', 'price': 19.99}]
            }

            self.assertDictEqual(store.json(), expected,
                                 f"The JSON export of the store is incorrect. Received {store.json()}, expected {expected}.")
