from tellr.db import db
from sqlalchemy.sql.expression import func, select

Model = db.Model


class AnswerModel(Model):

    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(40), nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_multiple(objects):
        db.session.bulk_save_objects(objects)
        db.session.commit()

    @classmethod
    def find_by_content(cls, _content, _question_id):
        return cls.query.filter(
            cls.content.ilike(_content), cls.question_id == _question_id
        ).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_wrong_answers(cls, question_id, correct_id):
        return (
            cls.query.order_by(func.random())
            .filter(cls.question_id == question_id, cls.id != correct_id)
            .limit(2)
        )
