from flask_restplus import Resource
from flask import request
from tellr.models.question import QuestionModel
from tellr.schemas.question import QuestionSchema
from tellr.models.answer import AnswerModel
from tellr.schemas.question_category import QuestionCategoryExtendedSchema
from tellr.models.question_category import QuestionCategoryModel

question_category_schema = QuestionCategoryExtendedSchema()
question_category_list_schema = QuestionCategoryExtendedSchema(many=True)
question_schema = QuestionSchema()
question_list_schema = QuestionSchema(many=True)


class GetQuestions(Resource):
    def get(self, category_id):
        category = QuestionCategoryModel.find_by_id(category_id)
        if category:
            questions = question_category_schema.dump(category)["questions"]
            return {"questions": questions}, 200

