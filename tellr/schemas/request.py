from tellr.ma import ma
from marshmallow import fields, validate
from tellr.models.request import RequestModel
from tellr.models.guess import GuessModel

ModelSchema = ma.ModelSchema


class GuessSchema(ModelSchema):
    class Meta:
        model = GuessModel
        include_fk = True


class RequestSchema(ModelSchema):
    class Meta:
        model = RequestModel
        include_fk = True
        dump_only = ("guesses",)

    guesses = ma.Nested(GuessSchema, many=True, exclude=("request_id", "id"))
