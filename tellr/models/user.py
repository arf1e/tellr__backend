from tellr.db import db

Model = db.Model
from datetime import date
from tellr.utils import calculate_age
from sqlalchemy.sql.expression import func, select
from tellr.models.line import LineModel
from tellr.models.decision import DecisionModel
from tellr.models.request import RequestModel
from tellr.models.contact import ContactModel


class UserModel(Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    # basic info
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    city = db.Column(db.String(40), nullable=False)
    city_id = db.Column(db.String(150), nullable=False)
    sex = db.Column(db.Boolean)
    first_name = db.Column(db.String(20))
    birthday = db.Column(db.DateTime, default=date(1997, 10, 16))
    description = db.Column(db.String(140))
    avatar = db.Column(db.String())
    avatar_big = db.Column(db.String())
    instagram = db.Column(db.String(30))
    vk = db.Column(db.String(32))

    lines = db.relationship("LineModel", lazy="dynamic")
    # topic
    hated = db.relationship(
        "DecisionModel",
        primaryjoin="and_(UserModel.id==DecisionModel.user_id, "
        "DecisionModel.hate==True)",
    )
    loved = db.relationship(
        "DecisionModel",
        primaryjoin="and_(UserModel.id==DecisionModel.user_id, "
        "DecisionModel.hate==False)",
    )
    # requests
    outvoices = db.relationship(
        "RequestModel",
        primaryjoin="and_(UserModel.id==RequestModel.asker_id, RequestModel.accepted==False)",
        lazy="dynamic",
    )
    invoices = db.relationship(
        "RequestModel",
        primaryjoin="and_(UserModel.id==RequestModel.receiver_id, RequestModel.accepted==False)",
        lazy="dynamic",
    )

    contacts = db.relationship(
        "ContactModel",
        primaryjoin="or_(UserModel.id==ContactModel.boy_id, UserModel.id==ContactModel.girl_id)",
    )
    # Essential db methods
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Some more db methods
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # fetch random users
    @classmethod
    def find_males(cls, list):
        return (
            cls.query.filter(~(cls.id.in_(list)), cls.sex == True, cls.lines != None)
            .order_by(func.random())
            .limit(4)
        )

    @classmethod
    def find_females(cls, list):
        return (
            cls.query.filter(~(cls.id.in_(list)), cls.sex == False, cls.lines != None)
            .order_by(func.random())
            .limit(4)
        )

    def get_lines(self, user_id):
        return self.lines(user_id=user_id)
