from tellr.ma import ma
from tellr.models.question import QuestionModel
from tellr.schemas.answer import AnswerSchema

ModelSchema = ma.ModelSchema


class QuestionSchema(ModelSchema):
    class Meta:
        model = QuestionModel
        include_fk = True

    answers = ma.Nested(AnswerSchema, many=True, exclude=("question_id",))
