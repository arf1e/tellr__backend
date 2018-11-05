#
# В этом проекте будет много комментариев, потому что я только-только вкатываюсь в питон и мне необходимо это делать
#
from flask import Flask, jsonify

# интерфейс бд
# я юзаю постгрес, так что для работы этой штуки за кадром еще нужен psycopg2
from flask_sqlalchemy import SQLAlchemy

# Инстанс
app = Flask(__name__)

# Конфигурации переехали
app.config.from_pyfile('./config.cfg', silent=True)

# Инстанс бд
db = SQLAlchemy(app)