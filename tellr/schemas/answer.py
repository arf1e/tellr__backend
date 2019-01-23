from tellr.ma import ma
from tellr.models.answer import AnswerModel

ModelSchema = ma.ModelSchema

class AnswerSchema(ModelSchema):
    class Meta:
      model = AnswerModel
      include_fk = True