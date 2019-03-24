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

    name = fields.String(required=True)
    age = fields.Integer(required=True)
    guesses = fields.Nested(
        GuessSchema,
        validate=validate.Length(min=1, error="No empty lists allowed"),
        many=True,
        required=True,
    )
