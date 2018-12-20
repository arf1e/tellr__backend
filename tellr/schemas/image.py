from marshmallow import Schema
from tellr.schemas.fields.filestorage import FileStorageField


class ImageSchema(Schema):
    image = FileStorageField(required=True)
