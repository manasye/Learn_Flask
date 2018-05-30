import sqlite3
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
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {'message': 'An error occured inserting the item'}, 500 # internal server error

        return item.json(), 201

    
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name, ))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:    
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occured inserting the item'}, 500 # internal server error

        else:
            try:
                updated_item.update()
            except:
                return {'message': 'An error occured updating the item'}, 500 # internal server error
		
        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
            
        connection.close()

        return {'items': items}
