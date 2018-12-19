from tellr.libs import image_helper
from marshmallow import fields
import uuid

class Avatar(fields.Field):
  def _serialize(self, value, attr, data):
    filename = str(uuid.uuid3(uuid.NAMESPACE_DNS, f'user_{value}'))
    folder = 'avatars'
    avatar_path = image_helper.find_image_any_format(filename, folder)
    if avatar_path:
      return avatar_path
    else:
      return image_helper.find_image_any_format('flower', folder)
