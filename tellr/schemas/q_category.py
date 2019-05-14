from tellr.ma import ma
from tellr.models.question_category import QuestionCategoryModel

ModelSchema = ma.ModelSchema


class QuestionCategorySchema(ModelSchema):
    class Meta:
        model = QuestionCategoryModel
        include_fk = True
