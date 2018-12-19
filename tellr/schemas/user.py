from tellr.ma import ma
from tellr.models.user import UserModel
from tellr.schemas.fields.age import Age
from tellr.schemas.fields.avatar import Avatar
from marshmallow import fields
ModelSchema = ma.ModelSchema
from tellr.libs import image_helper
class UserSchema(ModelSchema):
  class Meta:
    model = UserModel
    load_only = ('password', 'birthday')
    dump_only = ('id', 'age')

  # custom fields
  age = Age(attribute='birthday')
  avatar = Avatar(attribute='id')