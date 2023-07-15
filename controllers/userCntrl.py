from flask_restful import Resource
from flask import jsonify, request, current_app
from models.userModel import User
from werkzeug.security import generate_password_hash
import re

class UserCntrl(Resource):

    def __init__(self, **kwargs):
        self.db = kwargs['db']
 
    def get(self, user_id = None):

        if user_id:
            user = User.getUser_or_404(self.db,user_id)
            if user:
                return {
                    '_id' :user_id,
                    'name': user.name,
                    'email': user.email
                }
            else:
                return {"message": "user not found"}, 404
        
        else:
            users = self.db.users.find({})
            users_list = []
            for user in users:
                user['_id'] = str(user['_id'])
                users_list.append(user)
            return users_list, 200
        
         
    def post(self):

        try:
            name_pattern = r'^[A-Za-z\s\'.-]+$'
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            name = request.json['name']
            email = request.json['email']
            password = request.json['password']

            if not name or not email or not password:
                return {'message': "Data is missing required fields"}, 400
            
            if re.match(name_pattern,name) and re.match(email_pattern,email):

                new_user = User(name,email,password)
                registered_user = new_user.save(self.db)

                return registered_user,201
            else:
                return {"message": "Entered data is not valid"}, 400
        
        except Exception as e:

            return {"message": "Something went wrong"}, 500
        
    
    def put(self, user_id):
        
        try:
            name = request.json['name']
            email = request.json['email']
            password = request.json['password']

            if not name or not email or not password:
                return {'message': "Data is missing required fields"}, 400
 
            user = User.getUser_or_404(self.db,user_id)
            if user:

                user.name = name
                user.email = email
                if user.password == password:
                    user.password = password
                else:
                    user.password = generate_password_hash(password)

                
                if user.updateSingleUser(self.db,user_id):
                    return {
                        '_id': str(user_id),
                        'name': user.name,
                        'email': user.email
                    },200
                else:
                    return {'message': 'Failed to update user'}, 500
            else:
                return {"message": "user not found"}, 404
                
        
        except Exception as e:
            return {"message": "Something went wrong"}, 500
        

    def delete(self, user_id):

        try:
            ans = User.deleteSingleUser(self.db,user_id)
            print(type(ans))
            print(ans)
            if ans:
                return {"message": "Deleted Successfully"}, 200
            else:
                 return {"message": "Failed to delete"}, 500
        except Exception as e:
            return {"message": "Something went wrong"}, 500



