from tellr.ma import ma
from marshmallow import fields, validate
from tellr.models.request import RequestModel, BadgesInRequest
from tellr.models.guess import GuessModel
from tellr.schemas.badge import BadgeSchema

ModelSchema = ma.ModelSchema


class BadgesInRequestSchema(ModelSchema):
    class Meta:
        model = BadgesInRequest

    badge = ma.Nested(BadgeSchema, only=("id",))


class GuessSchema(ModelSchema):
    class Meta:
        model = GuessModel
        include_fk = True
        exclude = ("correct", "answer", "question")


class GuessExtendedSchema(ModelSchema):
    class Meta:
        model = GuessModel
        include_fk = True

    correct = ma.Nested("AnswerSchema", exclude=("id", "question_id"))
    answer = ma.Nested("AnswerSchema", exclude=("id", "question_id"))
    question = ma.Nested("QuestionSchema", only=("content",))


class RequestSchema(ModelSchema):
    class Meta:
        model = RequestModel
        include_fk = True
        dump_only = ("guesses",)

    guesses = ma.Nested(GuessSchema, many=True, exclude=("request_id", "id"))
    badges = ma.Nested(BadgesInRequestSchema, many=True, only=("badge",))


class RequestExtendedSchema(ModelSchema):
    class Meta:
        model = RequestModel
        include_fk = True
        dump_only = ("guesses",)

    guesses = ma.Nested(GuessExtendedSchema, many=True, exclude=("request_id", "id"))
    badges = ma.Nested(BadgesInRequestSchema, many=True, only=("badge",))
