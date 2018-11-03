#
# В этом проекте будет много комментариев, потому что я только-только вкатываюсь в питон и мне необходимо это делать
#
from flask import Flask, jsonify

# интерфейс бд
# я юзаю постгрес, так что для работы этой штуки за кадром еще нужен psycopg2
from flask_sqlalchemy import SQLAlchemy

# Инстанс
app = Flask(__name__)

# Конфигурации, которые потом все равно переедут в другие файлы
app.config['SECRET_KEY'] = 'i will move it to a gitignored file later anyway'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://snqnases:Ey09mFwY_muAv-rJMMoHCQRH10lgmFId@horton.elephantsql.com:5432/snqnases'

# Инстанс бд
db = SQLAlchemy(app)

# Накидаю пару моделей, пока что мне нужен МИНИМАЛЬНЕЙШИЙ функционал


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instagram_username = db.Column(db.String(30), unique=True, nullable=False)
    # Дамы и господа, связь 1:M
    questions = db.relationship('Question', backref='author', lazy=True)
    # backref - то, как на сущность user можно будет ссылаться из-под сущности вопроса
    # lazy - Когда будут загружены данные из бд. Так и написано в документации. ЯННП, но оставлю так
    # Еще нужно линкануть на сущность юзера из сущности вопроса

    def __repr__(self):
      # self в питоне почти то же самое что this в жаваскрипте
        # __repr__, а в джанго __str__ - Методы с ублюдским названием ( Как и полагается по ооп :) ),
        # которые описывают, как будут выглядеть сущности, выдаваемые по запросу
        return f"('{self.instagram_username}' хочет обкашлять вопросики: '{self.questions}'   )"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    choices = db.relationship('Choice', backref='question', lazy=True)
    correct_answer = db.relationship('Choice', uselist=False)

    def __repr__(self):
        return f"('{self.user_id.instagram_username}' задает вопрос '{self.question_text}' с вариантами ответа: '{self.choices}'"


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String(50), unique=True, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False)

    def __repr__(self):
        return f"(Вариант ответа '{self.choice_text}' для вопроса '{self.question.question_text}' )"

    # Эта штука для меня как для жс-макаки кажется сложной,
    # Но на самом деле __name__ == '__main__' - это проверка на то, что питону был скормлен именно этот файл
    # То есть буквально что в баше было прописано 'python tellr.py'
if __name__ == '__main__':
    app.run(debug=True)
