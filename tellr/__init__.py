import os
from flask import Flask, jsonify
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from tellr.db import db
from tellr.blacklist import BLACKLIST
from marshmallow import ValidationError
from flask_uploads import configure_uploads, patch_request_class
from tellr.libs.image_helper import IMAGE_SET
from dotenv import load_dotenv
from sqlalchemy import create_engine
from flask_migrate import Migrate

# Resources
from tellr.resources.user import UserRegister, User, UserLogin, UserLogout, UserQuery
from tellr.resources.image import AvatarUpload, Avatar
from tellr.resources.question import Question, Questions, FullQuestion
from tellr.resources.answer import Answer
from tellr.resources.line import LineCreate, Line, Lines
from tellr.resources.topic import Topic
from tellr.resources.decision import Decision
from tellr.resources.requests import Requests, Request
from tellr.resources.contacts import ContactList, Contact
from tellr.resources.self import Self
from tellr.resources.pusher import PusherAuth
from tellr.resources.badge import Badge, BadgeList
from tellr.resources.question_category import Category, CategoryList, CategoryCreate

# App instance
app = Flask(__name__)
# Config
app.config.from_object("tellr.default_config")
load_dotenv("tellr/.env")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URI", "sqlite:///data.db"
)
patch_request_class(app, 10 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)
api = Api(app)

jwt = JWTManager(app)
migrate = Migrate(app, db)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):  # except ValidationError as error
    return jsonify(err.messages), 400


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)

from tellr.scripts.load_questions import load_questions
from tellr.scripts.load_badges import load_badges

# load_questions()
# load_badges()


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserQuery, "/query")
api.add_resource(AvatarUpload, "/upload/avatar")
api.add_resource(Avatar, "/avatar/<int:user_id>")
api.add_resource(Question, "/question")
api.add_resource(Questions, "/questions")
api.add_resource(FullQuestion, "/questions/<int:question_id>")
api.add_resource(Answer, "/answer")
api.add_resource(LineCreate, "/line")
api.add_resource(Line, "/line/<int:line_id>")
api.add_resource(Lines, "/lines")
api.add_resource(Topic, "/topics")
api.add_resource(Decision, "/topic/<int:topic_id>")
api.add_resource(Requests, "/requests")
api.add_resource(Request, "/requests/<int:req_id>")
api.add_resource(ContactList, "/contacts")
api.add_resource(Contact, "/contacts/<int:contact_id>")
api.add_resource(Self, "/user/self")
api.add_resource(PusherAuth, "/pusher/auth")
api.add_resource(Badge, "/badge/<int:badge_id>")
api.add_resource(BadgeList, "/badges")
api.add_resource(Category, "/category/<int:category_id>")
api.add_resource(CategoryCreate, "/category")
api.add_resource(CategoryList, "/categories")
