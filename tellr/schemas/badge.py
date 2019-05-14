from tellr.ma import ma
from tellr.models.badge import BadgeModel

ModelSchema = ma.ModelSchema


class BadgeSchema(ModelSchema):
    class Meta:
        model = BadgeModel
