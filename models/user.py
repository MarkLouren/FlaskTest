import sqlite3

class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    @classmethod
    def find_by_usernsme(cls,username):  #cls - current class
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username =?"
        result = cursor.execute (query, (username,)) #username,)- show to python that we've created a tupple
        row =result.fetchone()
        if row:
            user = cls(*row) #the same as (row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls,_id):  #cls - current class
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id =?"
        result = cursor.execute (query, (_id,)) #username,)- show to python that we've created a tupple
        row =result.fetchone()
        if row:
            user = cls(*row) #the same as (row[0], row[1], row[2])
        else:
            user = None
        connection.close()
        return user