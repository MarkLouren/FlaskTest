import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sys
sys.path.insert(0, '/Users/vladymyrklykov/PycharmProjects/FlaskApi/code/models')
from item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()  # instead of json to be sure that only price past in no other
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="this field cannot be left blank!")


    @jwt_required()
    def get(self, name):
      item = ItemModel.find_by_name(name)
      if item:
            return item.json()
      else:
            return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])


        try:
          ItemModel.insert(item)

        except:
            return {"message": "An error ocurred inserting the item."}, 500

        return item.json(), 201


    def delete (self, name):  #delete item
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    def put (self, name):  #change item
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
               updated_item.insert()
            except:
                return {"message":" An error occurred inserting the item"}, 500
        else:
            try:
               updated_item.update()
            except:
                raise
                return {"message":" An error occurred updating the item"}, 500
        return updated_item.json()



class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items =[]
        for row in result:
            items.append({ 'name': row[0], 'price': row[1]
            })
        connection.close()

        return {'items': items}