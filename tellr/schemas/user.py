from tellr.ma import ma
from marshmallow import fields
from tellr.models.user import UserModel
from tellr.schemas.fields.age import Age

ModelSchema = ma.ModelSchema


class UserSchema(ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password", "birthday")
        dump_only = ("id", "age")

    # custom fields
    age = Age(attribute="birthday")
    lines = ma.Nested(
        "LineSchema",
        many=True,
        exclude=("user", "user_id", "correct_id", "question.answers"),
    )
    contacts = fields.Nested("ContactSchema", many=True)
    outvoices = fields.Pluck("RequestSchema", "receiver_id", many=True)
    invoices = ma.Nested("RequestSchema", many=True)
    hated = fields.Pluck("DecisionSchema", "topic_id", many=True)
    loved = fields.Pluck("DecisionSchema", "topic_id", many=True)


class UserStatsSchema(ModelSchema):
    class Meta:
        model = UserModel

    contacts = ma.Nested(
        "ContactExtendedSchema", only=("boy_request", "girl_request"), many=True
    )
    invoices = ma.Nested("RequestSchema", only=("badges",), many=True)
