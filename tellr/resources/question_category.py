from flask_restplus import Resource
from flask import request
from tellr.schemas.question_category import QuestionCategorySchema
from tellr.models.question_category import QuestionCategoryModel

question_category_schema = QuestionCategorySchema()
question_category_list_schema = QuestionCategorySchema(many=True)


class CategoryCreate(Resource):
    def post(self):
        category_json = request.get_json()
        category = question_category_schema.load(category_json)
        try:
            category.save_to_db()
        except:
            return {"msg": "Server error"}, 500
        return {"category": question_category_schema.dump(category)}, 201


class Category(Resource):
    def get(self, category_id):
        category = QuestionCategoryModel.find_by_id(category_id)
        if category:
            return {"category": question_category_schema.dump(category)}, 200
        return {"msg": "No category with such id"}

    def patch(self, category_id):
        category = QuestionCategoryModel.find_by_id(category_id)
        if category:
            category_json = request.get_json()
            if "title" in category_json.keys():
                category.title = category_json["title"]
            if "image" in category_json.keys():
                category.image = category_json["image"]
            if "description" in category_json.keys():
                category.description = category_json["description"]
            try:
                category.save_to_db()
            except:
                return {"message": "Database error"}, 500
        return {"category": question_category_schema.dump(category)}, 200

    def delete(self, category_id):
        category = QuestionCategoryModel.find_by_id(category_id)
        if category:
            try:
                category.delete_from_db()
            except:
                return {"msg": "Server error"}, 500
            return {"msg": "category deleted"}, 200
        else:
            return {"msg": "no category with such id"}, 404


class CategoryList(Resource):
    @classmethod
    def get(cls):
        categories = QuestionCategoryModel.find_all()
        return {"categories": question_category_list_schema.dump(categories)}, 200
