from tellr.ma import ma
from tellr.models.contact import ContactModel

ModelSchema = ma.ModelSchema


class ContactSchema(ModelSchema):
    class Meta:
        model = ContactModel
        include_fk = True

    boy = ma.Nested("UserSchema", only=("avatar", "id", "first_name"))
    girl = ma.Nested("UserSchema", only=("avatar", "id", "first_name"))


class ContactExtendedSchema(ModelSchema):
    class Meta:
        model = ContactModel
        include_fk = True

    boy = ma.Nested("UserSchema", only=("avatar", "id", "first_name"))
    boy_request = ma.Nested("RequestExtendedSchema")
    girl = ma.Nested("UserSchema", only=("avatar", "id", "first_name"))
    boy_request = ma.Nested("RequestExtendedSchema")
    girl_request = ma.Nested("RequestExtendedSchema")
