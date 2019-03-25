from tellr.db import db

Model = db.Model
from datetime import date
from tellr.utils import calculate_age
from sqlalchemy.sql.expression import func, select
from tellr.models.line import LineModel
from tellr.models.decision import DecisionModel


class UserModel(Model):
    __tablename__ = "users"

    # Поля
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    city = db.Column(db.String(40), default="Санкт-Петербург")
    # Определять пол булеаном меня научили еще в институте,
    # так что нихельпихель может написать своё приложение с гендерами и прочей хуетой
    sex = db.Column(db.Boolean)
    first_name = db.Column(db.String)
    birthday = db.Column(db.DateTime, default=date(1997, 10, 16))
    lines = db.relationship("LineModel", lazy="dynamic")
    hated = db.relationship("DecisionModel", primaryjoin="and_(UserModel.id==DecisionModel.user_id, " "DecisionModel.hate==True)")
    loved = db.relationship("DecisionModel", primaryjoin="and_(UserModel.id==DecisionModel.user_id, " "DecisionModel.hate==False)")

    # Essential db methods
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Some more db methods
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # fetch random users
    @classmethod
    def find_males(cls):
        return (
            cls.query.filter(cls.sex == True, cls.lines != None)
            .order_by(func.random())
            .limit(4)
        )

    @classmethod
    def find_females(cls):
        return (
            cls.query.filter(cls.sex == False, cls.lines != None)
            .order_by(func.random())
            .limit(4)
        )

    def get_lines(self, user_id):
        return self.lines(user_id=user_id)
