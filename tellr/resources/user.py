from flask_restplus import Resource, reqparse
from tellr.models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_raw_jwt,
    get_jwt_identity,
)
from tellr.blacklist import BLACKLIST


# TODO: Сделать разные парсеры для флоу регистрации и остальных, я сейчас слишком хочу спать даже для этого
user_parser = reqparse.RequestParser()
user_parser.add_argument("username", type=str, required=True, help="no username")
user_parser.add_argument("password", type=str, required=True, help="no password")
user_parser.add_argument("first_name", type=str)
user_parser.add_argument("sex", type=bool)


class UserRegister(Resource):
    def post(self):

        data = user_parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"msg": "user exists"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"msg": "user created"}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return (
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user.json()
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

        return user.json()

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
        jti = get_raw_jwt()["jti"]  # jti это "JWT ID", уникальный идентификатор JWT.
        # По нему можно однозначно идентифицировать пользователя, что позволяет реализовать систему логаутов.
        # Мы просто берём и добавляем этот идентификатор в блэклист, то есть тупо баним токен пользователя.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": f'User <id={user_id}> has logged out'}, 200


# Поиск
class UserQuery(Resource):
  @classmethod
  @jwt_required
  def get(cls):
    user_id = get_jwt_identity()
    user = UserModel.find_by_id(user_id).json()
    if user['sex'] == 'Male':
      users = [user.json() for user in UserModel.find_females()]
      return {'users': users}, 200
    else:
      users = [user.json() for user in UserModel.find_males()]
      return {'users': users}, 200

