from tellr.db import db
from tellr.models.question_category import QuestionCategoryModel

Model = db.Model


class QuestionModel(Model):

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), nullable=False, unique=True)
    answers = db.relationship("AnswerModel", lazy="dynamic", uselist=True)
    closed = db.Column(db.Boolean, default=False)

    category_id = db.Column(
        db.Integer, db.ForeignKey("question_categories.id"), nullable=False
    )
    category = db.relationship("QuestionCategoryModel")

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
    def get_questions(cls):
        return cls.query.all()
