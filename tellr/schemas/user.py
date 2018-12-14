from tellr.ma import ma
from tellr.models.user import UserModel
from tellr.schemas.fields.age import Age
ModelSchema = ma.ModelSchema

class UserSchema(ModelSchema):
  class Meta:
    model = UserModel
    load_only = ('password', 'birthday')
    dump_only = ('id', 'age')

  # custom fields
  age = Age(attribute='birthday')