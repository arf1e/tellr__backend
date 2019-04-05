from tellr.db import db
from sqlalchemy.sql.expression import func, select

Model = db.Model


class TopicModel(Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(30), unique=True, nullable=False)
    gif = db.Column(db.String, unique=True, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_topics(cls, list):
        return cls.query.filter(~(cls.id.in_(list))).limit(4)

    @classmethod
    def find_all(cls):
        return cls.query.all()
