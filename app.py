from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URL")
app.config["SECRET_KEY"] = os.getenv('SECRETKEY')

mongo = PyMongo(app)
db = mongo.db
api = Api(app)

from controllers.userCntrl import UserCntrl




api.add_resource(UserCntrl, '/users', '/users/<string:user_id>',resource_class_kwargs={'db': db})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)