from unittest import TestCase
from tellr.schemas.question_category import QuestionCategorySchema

category_schema = QuestionCategorySchema()


class UserTest(TestCase):
    def test_create_user(self):
        category = category_schema.load(
            {"title": "Вопросы для теста", "description": "Вопросы для теста"}
        )
        self.assertEqual(
            category.title,
            "Вопросы для теста",
            "Название категории не совпадает с ожидаемым",
        )
        self.assertEqual(
            category.description,
            "Вопросы для теста",
            "Описание категории не совпадает с ожидаемым",
        )
