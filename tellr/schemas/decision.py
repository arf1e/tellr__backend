from tellr.ma import ma
from tellr.models.decision import DecisionModel

ModelSchema = ma.ModelSchema


class DecisionSchema(ModelSchema):
    class Meta:
        model = DecisionModel
        include_fk = True
