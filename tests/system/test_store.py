from models.item import ItemModel
from tests.base_test import BaseTest
from models.store import StoreModel
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test_store')
                expected = {
                    'id': 1,
                    'name': 'test_store',
                    'items': []
                }
                self.assertEqual(response.status_code, 201,
                                 "The status_code of the response did not equal to 201 after create a new store.")

                self.assertIsNotNone(StoreModel.find_by_name('test_store'),
                                     "Did not find the store with name 'test_store' after create a new store.")

                self.assertIsNotNone(response.data,
                                     "The data of the response it's none after create a store.")

                self.assertDictEqual(expected, json.loads(response.data),
                                     f"The JSON of response {json.loads(response.data)} did not equal to expected {expected}")

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                response = client.post('/store/test_store')

                self.assertEqual(response.status_code, 400,
                                 "The status_code of response was not 400 after duplicate request.")

                self.assertDictEqual({'message': "A store with name 'test_store' already exists."},
                                     json.loads(response.data),
                                     "A store with that name did not already exists after register duplicate user")

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                resp = client.delete('/store/test_store')

                self.assertEqual(resp.status_code, 200,
                                 "The status_code of response was not 200 after delete request.")
                self.assertDictEqual(json.loads(resp.data), {'message': 'Store deleted'},
                                     f"The message after delete request did not equal expected. Actual {json.loads(resp.data)}")

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                resp = client.get('/store/test_store')
                expected = {
                    'id': 1,
                    'name': 'test_store',
                    'items': []
                }

                self.assertEqual(resp.status_code, 200,
                                 "The status_code of response was not 200 after get request.")
                self.assertDictEqual(json.loads(resp.data), expected,
                                     f"The JSON export of the store did not equal to expected {expected}. Received: {json.loads(resp.data)}")

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/store/test_store')
                expected = {'message': 'Store not found'}

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual(json.loads(resp.data), expected)

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/store/test_store')
                expected = {
                    'id': 1,
                    'name': 'test_store',
                    'items': [
                        {
                            'name': 'test',
                            'price': 19.99,
                        }
                    ]
                }

                self.assertEqual(resp.status_code, 200,
                                 "The status_code after get request did not equal to 200")
                self.assertDictEqual(json.loads(resp.data), expected,
                                     f"The JSON export of the store did not equal to expected {expected}. Received: {json.loads(resp.data)}")

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                resp = client.get('/stores')
                expected = {
                    'stores': [
                        {
                            'id': 1,
                            'name': 'test_store',
                            'items': []
                        }
                    ]
                }

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), expected,
                                     f"The JSON exports of the stores did not equal to expected. Expected {expected}.")

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()

                resp = client.get('/stores')
                expected = {
                    'stores': [
                        {
                            'id': 1,
                            'name': 'test_store',
                            'items': [{'name': 'test_item', 'price': 19.99}]
                        }
                    ]
                }

                self.assertEqual(resp.status_code, 200,
                                 f"The status_code after get request did not equal to 200. Actual {resp.status_code}")
                self.assertDictEqual(json.loads(resp.data), expected,
                                     f"The JSON exports did not equal to expected. Expected {expected}")
