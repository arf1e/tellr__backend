from marshmallow import fields
from tellr.utils import calculate_age

class Age(fields.Field):
  def _serialize(self, value, attr, data, **kwargs):
    return calculate_age(value)