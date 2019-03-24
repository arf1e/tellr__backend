from tellr.db import db
from sqlalchemy.sql.expression import func, select

Model = db.Model


class RequestModel(Model):

    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)

    asker_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    accepted = db.Column(db.Boolean, unique=False, default=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_outvoice(cls, user_id):
        return cls.query.filter_by(asker_id=user_id)

    @classmethod
    def get_invoice(cls, user_id):
        return cls.query.filter_by(receiver_id=user_id)

    @classmethod
    def find_existing(cls, asker_id, receiver_id):
      return cls.query.filter(cls.asker_id == asker_id, cls.receiver_id == receiver_id).first()
