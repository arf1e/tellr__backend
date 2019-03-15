from flask_restplus import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os
import uuid

from tellr.libs import image_helper
from tellr.schemas.image import ImageSchema
from tellr.schemas.user import UserSchema

image_schema = ImageSchema()
from tellr.models.user import UserModel


class AvatarUpload(Resource):
    @classmethod
    @jwt_required
    def put(cls):
        """
    Resource used to upload user avatars.
    This method should be idempotent, meaning uploading a new avatar
    overwrites the previous one.
    """

        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        filename = uuid.uuid3(uuid.NAMESPACE_DNS, f"user_{user_id}")
        folder = "avatars"
        # check if avatar already exists
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {"message": "avatar delete failed"}, 500
        try:
            ext = image_helper.get_extension(data["image"].filename)
            avatar = str(filename) + ext
            avatar_path = image_helper.get_path(
                image_helper.save_image(data["image"], folder=folder, name=avatar)
            )
            image_helper.resize(avatar_path)
            return {"message": f"avatar uploaded, path is {avatar_path}"}, 200
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": f"'{extension}' is an incorrect extension"}, 500


class Avatar(Resource):
    @classmethod
    def get(cls, user_id: int):
        folder = "avatars"
        filename = uuid.uuid3(uuid.NAMESPACE_DNS, f"user_{user_id}")
        avatar = image_helper.find_image_any_format(str(filename), folder)
        if avatar:
            return {"avatar": avatar}, 200
        return {"message": "avatar was not found"}, 404
