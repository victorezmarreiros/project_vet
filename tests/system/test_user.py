from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:  # para executar o teste passando-se por um cliente, é necessario self.app()
            with self.app_context():  # e para salvar as informações no banco de dados --> self.app_context()
                response = client.post('/register', data={'username': 'test', 'password': '1234'})  # doing post()

                self.assertEqual(response.status_code, 201,
                                 "The status code of response did not equal to 201")  # test response status_code

                self.assertIsNotNone(UserModel.find_by_username('test'),
                                     "Did not find a user with name 'test' after save_to_db.")  # test if save-to-db

                self.assertDictEqual({'message': 'User created successfully.'}, json.loads(response.data),
                                     "The JSON message that user was created is not equal to expected.")  # json msg

    # sempre que nós nos authenticamos '/auth', recebemos de volta um 'access_token' e sempre que a aplicação
    # exigir que o usuário esteja logado para acessar um end-point em particular,
    # nós teremos que enviar o 'access_token' --> json.loads(auth_request.data).keys()
    # para o end-point que queremos acessar e o Flask JWT será o responsável por verificar a authentificação para nós.
    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                # converting form data to json data, becuse '/auth' does not accept the form data, just json
                # -> data=json.dumps({'username': '<user>', 'password': '<password>'})
                # headers={'Content-Type': 'application/json'} --> definindo o tipo de dado que estamos enviando
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})
                self.assertIn('access_token', json.loads(auth_response.data).keys(),
                              f"Did not find a token of authentication after auth_request. Actual: {json.loads(auth_response.data).keys()}")
                # json.loads(auth_request.data).key() = ['access_token'] --> verificando se 'access_token' existe.
                # convertendo a authentificação do request em json e pegando as keys -> 'access_token'

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                # queremos apenas o response da segunda tentativa de registro
                # por isso armazenamos o response do nosso 2° post na variável response

                self.assertEqual(response.status_code, 400,
                                 "The status_code of response was not 400 after duplicate request.")

                self.assertDictEqual({'message': 'A user with that username already exists.'}, json.loads(response.data),
                                     "A user with that username did not already exists after register duplicate user")
