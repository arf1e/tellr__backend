from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from datetime import date

from tellr.models.user import UserModel
from tellr.schemas.user import UserSchema, SelfSchema
from tellr.libs.passwords import encrypt_password, check_encrypted_password

user_schema = UserSchema()
self_schema = SelfSchema()


class Self(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        return {"user": user_schema.dump(user)}, 200

    @classmethod
    @jwt_required
    def patch(cls):
        """
            Endpoint for changing any user info that won`t affect security.
        """
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        req_json = request.get_json()
        if "instagram" in req_json.keys():
            user.instagram = req_json["instagram"]
        if "vk" in req_json.keys():
            user.vk = req_json["vk"]
        if "birthday" in req_json.keys():
            bday = req_json["birthday"].split("-")
            user.birthday = date(int(bday[2]), int(bday[1]), int(bday[0]))
        try:
            user.save_to_db()
            return {"user": self_schema.dump(user)}, 200
        except:
            return {"message": "Database error"}, 500

    @classmethod
    @jwt_required
    def post(cls):
        """ 
            Endpoint for changing password.

        """
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        req_json = request.get_json()
        if check_encrypted_password(req_json["password"], user.password):
            user.password = encrypt_password(req_json["new_password"])
            user.save_to_db()
            return {"message": "password was updated"}, 200
        else:
            return {"message": "incorrect password"}, 402
