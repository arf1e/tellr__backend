from flask_restplus import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_raw_jwt,
    get_jwt_identity,
)
from tellr.models.user import UserModel
from tellr.schemas.user import UserSchema
from tellr.blacklist import BLACKLIST


user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


class UserRegister(Resource):
    def post(self):

        user_json = request.get_json()
        user_data = user_schema.load(user_json)
        user = user_data

        if UserModel.find_by_username(user.username):
            return {"msg": "user exists"}, 400

        user.save_to_db()
        return {"msg": "user created"}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_username(user_data.username)

        if user and safe_str_cmp(user.password, user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return (
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user_schema.dump(user)
                },
                200,
            )
        return {"msg": "invalid credentials"}, 400  # unauthorized


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg": "user not found"}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg": "user not found"}, 404
        user.delete_from_db()
        return {"msg": "user has been deleted"}, 200


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        print(get_raw_jwt()['jti'])
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", unique identifier for JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": f'User <id={user_id}> has logged out'}, 200


# Поиск
class UserQuery(Resource):
  @classmethod
  @jwt_required
  def get(cls):
    user_id = get_jwt_identity()
    user_data = UserModel.find_by_id(user_id)
    user = user_schema.dump(user_data)
    if user['sex'] == True:
      users = user_list_schema.dump(UserModel.find_females())
    else:
      users = user_list_schema.dump(UserModel.find_males()) 
    return {'users': users}, 200

