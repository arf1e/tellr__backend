from flask import Flask, jsonify
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from tellr.db import db
from tellr.blacklist import BLACKLIST
from marshmallow import ValidationError
from flask_uploads import configure_uploads, patch_request_class
from tellr.libs.image_helper import IMAGE_SET
from dotenv import load_dotenv
# Resources
from tellr.resources.user import UserRegister, User, UserLogin, UserLogout, UserQuery
from tellr.resources.image import AvatarUpload, Avatar

# App instance
app = Flask(__name__)
# Config
load_dotenv('tellr/.env', verbose=True) # Set your own env vars based on .env.example !
app.config.from_object('tellr.default_config')
app.config.from_envvar('APPLICATION_SETTINGS')
patch_request_class(app, 10 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)
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
api.add_resource(AvatarUpload, '/upload/avatar')
api.add_resource(Avatar, '/avatar/<int:user_id>')
