from tellr.db import db

Model = db.Model


class QuestionCategoryModel(Model):

    __tablename__ = "question_categories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False, unique=True)

    topcis = db.relationship("TopicModel", lazy="dynamic", uselist=True)

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
    def find_all(cls):
        return cls.query.all()

    def get_topics(self):
        return self.topics
