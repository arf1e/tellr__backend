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
        duplicate = AnswerModel.find_by_content(answer_json["content"])
        if duplicate:
            return {"answer": answer_schema.dump(duplicate)}, 200
        try:
            answer.save_to_db()
            answer_entity = answer_schema.dump(answer)
        except:
            return {"msg": "Server error"}, 500
        return {"answer": answer_entity}, 201
