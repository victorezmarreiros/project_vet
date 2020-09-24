from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):

    def setUp(self):                                                            # authenticação de usuário
        super(ItemTest, self).setUp()                 # chamando o metodo setUp() após herdar a super() classe ItemTest
        with self.app() as client:                                              # setUp() roda sempre antes de cada test
            with self.app_context():
                UserModel('test_user', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test_user', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test_item')
                self.assertEqual(resp.status_code, 401,  # Cod: 401, Response: usuário não está authenticado-jwt
                                 "The status_code after get '/item/test_item' did not equal to 401 as expected.")

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test_item', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404,  # Cod 404 default for Not Found.
                                 "The status_code after get '/item/test_item' did not equal to 404 as expected.")

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()
                resp = client.get('/item/test_item', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200,
                                 "The status_code after get '/item/test_item' did not equal to 200 as expected.")

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()
                resp = client.delete('/item/test_item')
                expected = {'message': 'Item deleted'}

                self.assertEqual(resp.status_code, 200,
                                 "The status_code after delete '/item/test_item' did not equal to 201 as expected.")
                self.assertDictEqual(expected, json.loads(resp.data),
                                     "The message after delete request did not equal to " 
                                     f"Expected {expected} != "
                                     f"Actual {json.loads(resp.data)}")

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                resp = client.post('/item/test_item', data={'price': 17.99, 'store_id': 1})
                expected = {'name': 'test_item', 'price': 17.99}

                self.assertEqual(resp.status_code, 201,
                                 "The status_code after post '/item/test_item' did not equal to 201 as expected.")

                self.assertDictEqual(expected, json.loads(resp.data),
                                     "The message after delete request did not equal to " 
                                     f"Expected {expected} != "
                                     f"Actual {json.loads(resp.data)}")

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 17.99, 1).save_to_db()

                resp = client.post('/item/test_item', data={'price': 17.99, 'store_id': 1})
                expected = {'message': "An item with name 'test_item' already exists."}

                self.assertEqual(resp.status_code, 400,
                                 "The status_code after post '/item/test_item' did not equal to 400 as expected.")

                self.assertDictEqual(expected, json.loads(resp.data),
                                     "The message after delete request did not equal to "
                                     f"Expected {expected} != "
                                     f"Actual {json.loads(resp.data)}")

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                resp = client.put('/item/test_item', data={'price': 17.99, 'store_id': 1})
                expected = {'name': 'test_item', 'price': 17.99}

                self.assertEqual(resp.status_code, 200,
                                 "The status_code after put '/item/test_item' did not equal to 200 as expected.")

                self.assertEqual(json.loads(resp.data), expected,
                                 "The JSON exports after put request did not equal to "
                                 f"Expected {expected} != "
                                 f"Actual {json.loads(resp.data)}")

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 5.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test_item').price, 5.99,
                                 "The price of the item did not equal to 5.99.")

                resp = client.put('/item/test_item', data={'price': 17.99, 'store_id': 1})
                expected = {'name': 'test_item', 'price': 17.99}

                self.assertEqual(resp.status_code, 200,
                                 "The status_code after put '/item/test_item' did not equal to 200 as expected.")

                self.assertEqual(ItemModel.find_by_name('test_item').price, 17.99,
                                 "The price of the item did not equal to 17.99.")

                self.assertDictEqual(expected, json.loads(resp.data),
                                     "The JSON exports after put request did not equal to "
                                     f"Expected {expected} != "
                                     f"Actual {json.loads(resp.data)}")

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 17.99, 1).save_to_db()

                resp = client.get('/items')
                expected = {
                    'items': [
                        {
                            'name': 'test_item',
                            'price': 17.99
                        }
                    ]
                }
                self.assertDictEqual(expected, json.loads(resp.data),
                                     "The JSON exports after put request did not equal to "
                                     f"Expected {expected} != "
                                     f"Actual {json.loads(resp.data)}")
