from marshmallow import fields
from werkzeug.datastructures import FileStorage

class FileStorageField(fields.Field):
  def _deserialize(self, value, attr, data):
    default_error_messages = {
      "invalid": "Not a valid image."
    }

    if value is None:
      return None
    
    if not isinstance(value, FileStorage):
      self.fail("invalid") # will throw ValidationError with default_error_messages["invalid"]`s message

    return value 