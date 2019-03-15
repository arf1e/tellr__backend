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
from tellr.resources.question import Question, Questions
from tellr.resources.answer import Answer
from tellr.resources.line import LineCreate, Line, Lines

# App instance
app = Flask(__name__)
# Config
app.config.from_object("tellr.default_config")
patch_request_class(app, 10 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)
api = Api(app)

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):  # except ValidationError as error
    return jsonify(err.messages), 400


@app.before_first_request
def create_tables():
    db.create_all()


from tellr.db import db

db.init_app(app)


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserQuery, "/query")
api.add_resource(AvatarUpload, "/upload/avatar")
api.add_resource(Avatar, "/avatar/<int:user_id>")
api.add_resource(Question, "/question")
api.add_resource(Questions, "/questions")
api.add_resource(Answer, "/answer")
api.add_resource(LineCreate, "/line")
api.add_resource(Line, "/line/<int:line_id>")
api.add_resource(Lines, "/lines")
