from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

    @jwt_required()     # -> a função retorna cod: 401 caso o usuário não esteja logado antes do request get('/item/<>')
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name {name!r} already exists."}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()               # --> headers=data{'price': 1.99, 'store_id': 1}

        item = ItemModel.find_by_name(name)           # --> Encontrando Item no banco pesquisando pelo nome.

        if item is None:                              # --> se o item não existir, cria o item
            item = ItemModel(name, **data)
        else:                                         # --> se não,
            if item.price == data['price']:           #  -> se o preço do item no bdd for igual ao headers=data['price']
                return f"The item already exists. Item: {item.json()}", 400     # --> O Item já existe, 400

            item.price = data['price']                #  -> se não, atualiza o preço do item

        item.save_to_db()                            # --> ao acabar a verificação, salva no banco de dados

        return item.json()                           # --> retorna o item .json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
