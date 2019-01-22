from flask_restplus import Resource
from flask import request
from tellr.schemas.answer import AnswerSchema

answer_schema = AnswerSchema()

class Answer(Resource):
  def post(self):
    answer_json = request.get_json()
    answer = answer_schema.load(answer_json)
    try:
      answer.save_to_db()
    except:
      return {"msg": "Server error"}, 500
    return {"msg": "answer added"}, 201