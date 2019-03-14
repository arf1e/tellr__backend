from flask_restplus import Resource
from flask import request
from tellr.schemas.answer import AnswerSchema
from tellr.models.answer import AnswerModel

answer_schema = AnswerSchema()
answer_list_schema = AnswerSchema(many=True)


class Answer(Resource):
    def post(self):
        answer_json = request.get_json()
        answer = answer_schema.load(answer_json)
        try:
            answer.save_to_db()
        except:
            return {"msg": "Server error"}, 500
        return {"msg": "answer added"}, 201

    def get(self):
        answers = answer_list_schema.dump(
            AnswerModel.get_wrong_answers(question_id=2, correct_id=1)
        )
        return {"answers": answers}, 200
