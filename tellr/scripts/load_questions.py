from tellr.models.question_category import QuestionCategoryModel
from tellr.models.question import QuestionModel
from tellr.schemas.question_category import QuestionCategorySchema
from tellr.schemas.question import QuestionSchema
from tellr.db import db
from tellr import app

category_list_schema = QuestionCategorySchema(many=True)
question_list_schema = QuestionSchema(many=True)

categories = [
    {
        "title": "Вопросы Дудя",
        "image": "https://cdn21.img.ria.ru/images/150978/16/1509781669_312:45:1736:852_600x0_80_0_0_0acb230165c35f4b24e7ee06a44c5cb2.png",
        "description": "Никому никогда не было интересно сколько вы зарабатываете? Этот и другие вопросы здесь.",
    },
    {"title": "Общие вопросы"},
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
