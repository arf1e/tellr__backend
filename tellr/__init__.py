from flask import Flask
from flask_restplus import Api
from flask_jwt_extended import JWTManager

from tellr.db import db

# Инстанс
app = Flask(__name__)
# Конфигурации переехали
app.config.from_pyfile('./config.cfg', silent=True)
api = Api()

@app.before_first_request
def create_tables():
  db.create_all()