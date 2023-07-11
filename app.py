from flask import Flask, jsonify, request
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from flask_pymongo import PyMongo
from dotenv import load_dotenv
load_dotenv()
import os
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URL")
app.config["SECRET_KEY"] = os.getenv('SECRETKEY')

mongo = PyMongo(app)
db = mongo.db

@app.route("/users", methods = ["GET", "POST"])

def get_all_users_or_add():

    if request.method == "GET":
        try:
            users = db.user.find({})
            return dumps(users),200
        except Exception as e:
            return jsonify({"message": "Something went wrong"}), 500
    
    if request.method == "POST":
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        if not name or not email or not password:
            return jsonify({"status": 403, "message": "All fields are mandatory"})
        else:

            user = db.user.find_one({'email': email})

            if user is not None:
                return jsonify({"message": "Account already exists"}), 403
            

            hashed_pwd = generate_password_hash(password)
            try:
                db.user.insert_one({"email":email, "name":name,"password": hashed_pwd})
                return jsonify({"message": "User created successfully"}),201
            except Exception as e:
                return jsonify({"message": "Failed to execute"}), 400



@app.route("/users/<id>",methods = ["DELETE", "PUT", "GET"])
def perform_operation(id):
    
    if request.method == "GET":
        user = db.user.find_one({'_id': ObjectId(id)})

        if user is None:
            return jsonify({"message": f"User with id: {id} does not exists"}), 404
        else:
            return dumps(user), 200
    
    if request.method == "PUT":
        user = db.user.find_one({'_id': ObjectId(id)})

        if user is None: 
            return jsonify({"message": f"User with id: {id} does not exists"}), 404
        
        
        if "name" in request.json:
            name = request.json["name"]
        else:
            name = user["name"]

        if "email" in request.json:
            email = request.json["email"]
        else:
            email = user["email"]

        if "password" in request.json:
            password = request.json["password"]
            hashed_pwd = generate_password_hash(password)
        else:
            hashed_pwd = user["password"]



        
        db.user.update_one({'_id': ObjectId(id)}, {'$set': {'name':name, 'email': email, 'password': hashed_pwd}})
        return jsonify({"message": f"User with id: {id} updated successfully"}), 200
       
    
    if request.method == "DELETE":
        try:
            user = db.user.find_one({'_id': ObjectId(id)})

            if user is None: 
                return jsonify({"message": f"User with id: {id} does not exists"}), 404
            
            db.user.delete_one({"_id": ObjectId(id)})
            return jsonify({"message": "User deleted successfully"}), 200
        except Exception as e:
            return jsonify({"message": "Something went wrong"}), 500


if __name__ == "__main__":
    app.run(debug=True)