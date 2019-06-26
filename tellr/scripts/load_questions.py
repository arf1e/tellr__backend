from tellr.models.question_category import QuestionCategoryModel
from tellr.models.question import QuestionModel
from tellr.schemas.question_category import QuestionCategorySchema
from tellr.schemas.question import QuestionSchema
from tellr.db import db
from tellr import app

category_list_schema = QuestionCategorySchema(many=True)
question_list_schema = QuestionSchema(many=True)


badges = [
    {"title": "Красивый", "title_f": "Красивая", "emoji": "+1"},
    {"title": "Милый", "title_f": "Милая", "emoji": "cat"},
    {"title": "Хот", "title_f": "Хот", "emoji": "fire"},
    {"title": "Скромный", "title_f": "Скромная", "emoji": "flushed"},
    {"title": "Тусовщик", "title_f": "Тусовщица", "emoji": "tada"},
    {"title": "Творческий", "title_f": "Творческая", "emoji": "art"},
]

categories = [
  {"title": "Общие вопросы"}
]

questions = [
  {"content": "Оказавшись перед Путиным, что ты ему скажешь?", "category_id": 1},
  {"content": "Путин красавчик?", "category_id": 1},
  {"content": "Когда последний раз дрался?", "category_id": 1},
  {"content": "Твоё любимое время года?", "category_id": 2},
  {"content": "Есть кот?", "category_id": 2},
  {"content": "Хочешь известности? Почему?", "category_id": 2},
  {"content": "Были мысли о суициде?", "category_id": 2},
]


def load_questions():
    with app.app_context():
        db.create_all()
        db.session.bulk_save_objects(category_list_schema.load(categories))
        db.session.commit()
        db.session.bulk_save_objects(question_list_schema.load(questions))
        db.session.commit()
        return {"message": "questions were loaded into db"}
