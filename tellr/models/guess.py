from tellr.db import db
from sqlalchemy.sql.expression import func, select

Model = db.Model


class GuessModel(Model):

    __tablename__ = "guesses"

    id = db.Column(db.Integer, primary_key=True)

    request_id = db.Column(db.Integer, db.ForeignKey("requests.id"), nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    correct_id = db.Column(db.Integer, db.ForeignKey("answers.id"), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey("answers.id"), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
