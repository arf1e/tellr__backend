from flask import Flask, jsonify
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from tellr.db import db
from tellr.blacklist import BLACKLIST
from marshmallow import ValidationError
# Resources
from tellr.resources.user import UserRegister, User, UserLogin, UserLogout, UserQuery

# App instance
app = Flask(__name__)
# Config file
app.config.from_pyfile("./config.py", silent=True)
api = Api(app)

jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err): # except ValidationError as error
    return jsonify(err.messages), 400


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogout, '/logout')
api.add_resource(UserQuery, '/query')
