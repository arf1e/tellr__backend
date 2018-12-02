from db import db
Model = db.Model

class ChoiceModel(Model):
  __tablename__ = 'choices'

  id = db.Column(db.Integer, primary_key = True)
  choice_text = db.Column(db.String(255))

  question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
  question = db.relationship('QuestionModel')

  def __init__(self, choice_text, question_id):
    self.choice_text = choice_text
    self.question_id = question_id
  
  def json(self):
    return {
      'id': self.id,
      'choice_text': self.choice_text,
      'question_id': self.question_id
    }

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()
  
  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()