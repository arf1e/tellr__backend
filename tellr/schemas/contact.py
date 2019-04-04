from tellr.ma import ma
from tellr.models.contact import ContactModel

ModelSchema = ma.ModelSchema


class ContactSchema(ModelSchema):
    class Meta:
        model = ContactModel
        include_fk = True
