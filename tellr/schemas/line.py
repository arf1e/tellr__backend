from marshmallow import fields
from tellr.ma import ma
from tellr.schemas.question import QuestionSchema, AnswerSchema
from tellr.schemas.user import UserSchema
from tellr.models.line import LineModel
from tellr.schemas.question_category import QuestionCategorySchema

ModelSchema = ma.ModelSchema


class LineSchema(ModelSchema):
    class Meta:
        model = LineModel
        include_fk = True
        exclude = ("user",)

    correct = ma.Nested(AnswerSchema, exclude=("question_id",))
    question = ma.Nested(QuestionSchema, exclude=("answers",))


class LineExtendedSchema(ModelSchema):
    class Meta:
        model = LineModel
        include_fk = True
        exclude = ("user",)

    correct = ma.Nested(AnswerSchema, exclude=("question_id",))
    question = ma.Nested(QuestionSchema, exclude=("answers",))
