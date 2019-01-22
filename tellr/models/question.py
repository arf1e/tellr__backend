from tellr.db import db

Model = db.Model

class QuestionModel(Model):
  
  __tablename__ = 'questions'

  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(40), nullable=False, unique=True)
  answers = db.relationship('AnswerModel', lazy="dynamic")

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