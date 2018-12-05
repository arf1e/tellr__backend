from flask import Flask
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from tellr.db import db

# resources
from tellr.resources.user import UserRegister, User, UserLogin
# Инстанс
app = Flask(__name__)
# Конфигурации переехали
app.config.from_pyfile('./config.cfg', silent=True)
api = Api(app)

jwt = JWTManager(app)

@app.before_first_request
def create_tables():
  db.create_all()

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(User, '/user/<int:user_id>')