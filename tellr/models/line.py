from tellr.db import db
from tellr.models.question import QuestionModel
from tellr.models.answer import AnswerModel

Model = db.Model


class LineModel(Model):
    __tablename__ = "lines"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    question = db.relationship("QuestionModel")

    correct_id = db.Column(db.Integer, db.ForeignKey("answers.id"))
    correct = db.relationship("AnswerModel", lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_lines(cls):
        return cls.query.all()
