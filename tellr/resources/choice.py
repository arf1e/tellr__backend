from flask_restplus import Resource, reqparse
from models.choice import ChoiceModel
from models.question import QuestionModel

class Choice(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('choice_text', type=str, required=True, help='Это поле не может быть пустым')
  parser.add_argument('question_id', type=int)

  def post(self, question_id):
    # Если для этого вопроса уже существует такой ответ, то мы его не примем.
    question = QuestionModel.find_by_id(question_id)
    if question:
      data = Choice.parser.parse_args()
      choice = ChoiceModel()