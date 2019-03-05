
from models.user import UserModel

def authenticate(username, password):  #authentication of a user
    user = UserModel.find_by_usernsme(username)
    if user and user.password == password:  #check it
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
