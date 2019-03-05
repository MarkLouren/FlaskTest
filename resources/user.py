import sys
sys.path.insert(0, '/Users/vladymyrklykov/PycharmProjects/FlaskApi/code/models')
from user import UserModel
import sqlite3
from flask_restful import Resource,reqparse

class UserRegister(Resource):
#method should addd new users to db
    parser=reqparse.RequestParser()  #Parse the Json request check username and password
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="this field cannot be blank")

    parser.add_argument('password',
                    type=str,
                    required=True,
                    help="this field cannot be blank")
    def post (self):
        data=UserRegister.parser.parse_args()  #get data from the parser
        if UserModel.find_by_usernsme(data['username']):  #help to avoid dublicate users, check if user=None than..put before connection, or it never close
            return {"message":"A user with that username already exists"},400
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)" #NUL: because id is auto incrementing
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()
        return {"message": "User was created sucessfully"}, 201