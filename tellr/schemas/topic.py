from tellr.ma import ma
from tellr.models.topic import TopicModel

ModelSchema = ma.ModelSchema


class TopicSchema(ModelSchema):
    class Meta:
        model = TopicModel
        include_fk = True
