from tellr.db import db
from sqlalchemy.sql.expression import func, select

Model = db.Model


class DecisionModel(Model):
    __tablename__ = "decisions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False)
    hate = db.Column(db.Boolean)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_hated(id):
        return cls.query.filter(user_id=id, hate=True)

    @classmethod
    def get_loved(id):
        return cls.query.filter(user_id=id, hate=False)

    @classmethod
    def find_by_id(id):
        return cls.query.filter_by(id=id).first()
