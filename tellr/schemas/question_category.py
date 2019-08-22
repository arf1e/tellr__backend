from tellr.ma import ma
from tellr.models.question_category import QuestionCategoryModel
from tellr.schemas.question import QuestionSchema

ModelSchema = ma.ModelSchema


class QuestionCategorySchema(ModelSchema):
    class Meta:
        model = QuestionCategoryModel
        include_fk = True


class QuestionCategoryExtendedSchema(ModelSchema):
    class Meta:
        model = QuestionCategoryModel
        include_fk = True

    questions = ma.Nested("QuestionSchema", many=True, exclude=("category_id",))
