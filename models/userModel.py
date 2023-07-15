from flask_pymongo import ObjectId
from werkzeug.security import generate_password_hash


class User:

    def __init__(self,name: str,email: str,password: str):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def save(self,db):
        new_user = db.users.insert_one({
            'name': self.name,
            'email': self.email,
            'password': self.password
        })

        dic = {
            '_id': str(new_user.inserted_id),
            'name': self.name,
            'email': self.email,
            'password': self.password
        }
        return dic
    
    def getUser_or_404(db,user_id):
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            return User(user['name'],user['email'], user['password'])
        else:
            return None
        
    def updateSingleUser(self,db, user_id):
        update_user = db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'name': self.name, 'email': self.email, 'password': self.password}})
        return update_user.modified_count > 0
    
    def deleteSingleUser(db, user_id):
        print("hello2")
        deleted_user = db.users.delete_one({'_id': ObjectId(user_id)})
        print("hello")
        return deleted_user.deleted_count > 0
