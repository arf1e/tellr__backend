from tellr import db
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
        return f"('{self.instagram_username}', '{self.questions}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    choices = db.relationship('Choice', backref='question', lazy=True)
    # correct_answer = db.relationship('Choice', uselist=False)

    def __repr__(self):
        return f"(вопрос '{self.question_text}' с вариантами ответа: '{self.choices}')"


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String(50), unique=True, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False)

    def __repr__(self):
        return f"(Вариант ответа '{self.choice_text}' для вопроса '{self.question.question_text}' )"