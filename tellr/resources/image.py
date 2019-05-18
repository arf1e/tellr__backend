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
        request_json = request.get_json()  # {"avatar": link}
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if user:
            print(request_json)
            user.avatar = request_json["avatar"]
            user.avatar_big = request_json["avatar_big"]
            user.save_to_db()
            return {"message": "avatar updated"}, 200


class Avatar(Resource):
    @classmethod
    def get(cls, user_id: int):
        """
        Resource that sends avatar of given user.
        """
        user = UserModel.find_by_id(user_id)
        if user.avatar:
            return {"avatar": user.avatar}, 200
        return {"message": "avatar was not found"}, 404
