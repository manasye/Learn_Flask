from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float,
        required=True,
        help="This field can not be blank!"
    )
	
    parser.add_argument('store_id', 
        type=int,
        required=True,
        help="Every item need store id."
    )

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occured searching the item'}, 500

        if item:
            return item.json()

        return {'message': 'Item not found'}, 404 # not-found

    
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name "{}" already exists.' . format(name)}, 400 # bad-request

        data = Item.parser.parse_args() 
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item'}, 500 # internal server error

        return item.json(), 201

    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:    
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
		
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
