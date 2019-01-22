from flask_restplus import Resource
from flask import request
from tellr.models.question import QuestionModel
from tellr.schemas.question import QuestionSchema

question_schema = QuestionSchema()
question_list_schema = QuestionSchema(many=True)

class Question(Resource):
  def post(self):
    question_json = request.get_json()
    question = question_schema.load(question_json)
    question.save_to_db()
    return {"msg": "question added"}, 201


class Questions(Resource):
  def get(self):
    questions = question_list_schema.dump(QuestionModel.get_questions())
    return {"questions": questions}, 200