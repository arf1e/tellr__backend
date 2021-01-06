from flask_restplus import Resource
from flask import request
from flask_jwt_extended import jwt_required

from tellr.schemas.answer import AnswerSchema
from tellr.models.answer import AnswerModel
answer_schema = AnswerSchema()
answer_list_schema = AnswerSchema(many=True)


class Answer(Resource):
    @jwt_required
    def post(self):
        """
        Answer creation resource.
        Expected request body: {
            question_id: int, 
            content: "str"
        }
        """
        answer_json = request.get_json()
        answer = answer_schema.load(answer_json)
        duplicate = AnswerModel.find_by_content(
            answer_json["content"], answer_json["question_id"]
        )
        if duplicate:
            return {"answer": answer_schema.dump(duplicate)}, 200
        try:
            answer.save_to_db()
            answer_entity = answer_schema.dump(answer)
        except:
            return {"msg": "Server error"}, 500
        return {"answer": answer_entity}, 201


class UpdateAnswer(Resource):
    @classmethod
    def delete(cls, answer_id):
        answer = AnswerModel.find_by_id(answer_id)
        if answer:
            try:
                answer.delete_from_db()
            except:
                return {"msg": "Server error"}, 500
            return {"msg": "Answer was successfully removed"}, 200
        else:
            return {"msg": "Answer was not found"}, 404
