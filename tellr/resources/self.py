from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from tellr.models.user import UserModel
from tellr.schemas.user import UserSchema

user_schema = UserSchema()

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
        if "instagram" in req_json:
            user.instagram = req_json["instagram"]
        if "vk" in req_json:
            user.vk = req_json["vk"]
        try:
            user.save_to_db()
            return {"user": user_schema.dump(user)}, 200
        except:
            return {"message": "Database error"},500
        

