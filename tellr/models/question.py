from tellr.db import db
Model = db.Model

class QuestionModel(Model):
  __tablename__ = 'questions'

  id = db.Column(db.Integer, primary_key=True)
  question_text = db.Column(db.String(200), nullable=False)
  choices = db.relationship('ChoiceModel', backref='question', lazy='dynamic')

  correct = db.Column(db.Integer)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  user = db.relationship('UserModel')

  def __init__(self, question_text, correct, user_id):
    self.question_text = question_text
    self.correct = correct
    self.user_id = user_id

  # Служебные методы
  def json(self):
    return {
      'id': self.id,
      'question_text': self.question_text
      'user_id': self.user_id
      'choices': [choice.json() for choice in self.choices.all()]
      'correct': self.choices[self.correct]
    }
  
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()
  
  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def find_by_question_text(cls, question_text):
    return cls.query.filter_by(question_text=question_text).first()
  
  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()