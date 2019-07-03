from flask_restplus import Resource
from flask import request
from tellr.models.question import QuestionModel
from tellr.schemas.question import QuestionSchema
from tellr.schemas.user import UserSchema
from tellr.models.answer import AnswerModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from tellr.models.user import UserModel

question_schema = QuestionSchema()
user_schema = UserSchema()
question_list_schema = QuestionSchema(many=True)


class Question(Resource):
    def post(self):
        question_json = request.get_json()
        question = question_schema.load(question_json)
        question.save_to_db()
        return {"msg": "question added"}, 201


class RandomQuestion(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        if user_id is None:
            return {"msg": "Authorization required"}, 401
        user = UserModel.find_by_id(user_id)
        user_lines = user_schema.dump(user)["lines"]
        questions = []
        for line in user_lines:
            questions.append(line["question"]["id"])
        question = QuestionModel.find_random(questions)
        return {"question": question_schema.dump(question)}, 200


class Questions(Resource):
    def get(self):
        questions = question_list_schema.dump(QuestionModel.get_questions())
        return {"questions": questions}, 200


class FullQuestion(Resource):
    def get(self, question_id):
        question = QuestionModel.find_by_id(question_id)
        if question:
            return {"question": question_schema.dump(question)}
        return {"message": "question was not found"}, 404

    def delete(self, question_id):
        question = QuestionModel.find_by_id(question_id)
        if question:
            question.delete_from_db()
        return {"msg": "question removed"}, 200

    def patch(self, question_id):
        question = QuestionModel.find_by_id(question_id)
        if question:
            question_json = request.get_json()
            question.content = question_json["content"]
            question.save_to_db()
        return {"msg": "question updated"}, 200
