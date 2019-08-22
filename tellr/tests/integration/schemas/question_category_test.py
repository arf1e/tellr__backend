from tellr.schemas.question_category import QuestionCategorySchema
from tellr.models.question_category import QuestionCategoryModel
from tellr.tests.base_test import BaseTest

category_schema = QuestionCategorySchema()


class UserTest(BaseTest):
    def test_category_crud(self):
        with self.app_context():
            category = category_schema.load(
                {"title": "Вопросы для теста", "description": "Вопросы для теста"}
            )

            self.assertIsNone(QuestionCategoryModel.find_by_id(1))

            category.save_to_db()

            self.assertIsNotNone(QuestionCategoryModel.find_by_id(1))

            category_dump = category_schema.dump(QuestionCategoryModel.find_by_id(1))

            self.assertEqual(category_dump["title"], "Вопросы для теста")
            self.assertEqual(category_dump["description"], "Вопросы для теста")

            category.delete_from_db()

            self.assertIsNone(QuestionCategoryModel.find_by_id(1))
