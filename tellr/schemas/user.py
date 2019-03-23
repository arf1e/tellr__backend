from tellr.ma import ma
from tellr.models.user import UserModel
from tellr.schemas.fields.age import Age
from tellr.schemas.fields.avatar import Avatar

ModelSchema = ma.ModelSchema


class UserSchema(ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password", "birthday")
        dump_only = ("id", "age")

    # custom fields
    age = Age(attribute="birthday")
    avatar = Avatar(attribute="id")
    lines = ma.Nested(
        "LineSchema",
        many=True,
        exclude=("user", "user_id", "correct_id", "question.answers"),
    )
