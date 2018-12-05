from flask_restplus import Resource, reqparse
from tellr.models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token


# TODO: Сделать разные парсеры для флоу регистрации и остальных, я сейчас слишком хочу спать даже для этого
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help='no username')
_user_parser.add_argument('password', type=str, required=True, help='no password')
_user_parser.add_argument('first_name', type=str)
_user_parser.add_argument('sex', type=bool)

class UserRegister(Resource):
  def post(self):
    data = _user_parser.parse_args()
    if UserModel.find_by_username(data['username']):
      return {'msg': 'user exists'}, 400
    user = UserModel(**data)
    user.save_to_db()
    return {'msg': 'user created'}, 201

class UserLogin(Resource):
  @classmethod
  def post(cls):
    data = _user_parser.parse_args()
    user = UserModel.find_by_username(data['username'])
    if user and safe_str_cmp(user.password, data['password']):
      access_token = create_access_token(identity=user.id, fresh=True)
      refresh_token = create_refresh_token(user.id)
      return {
        'access_token': access_token,
        'refresh_token': refresh_token
      }, 200
    return {'msg': 'invalid credentials'}, 400 # unauthorized

class User(Resource):
  @classmethod
  def get(cls, user_id):
    user = UserModel.find_by_id(user_id)
    if not user:
      return {'msg': 'user not found'}, 404
    
    return user.json()
  
  @classmethod
  def delete(cls, user_id):
    user = UserModel.find_by_id(user_id)
    if not user:
      return {'msg': 'user not found'}, 404
    user.delete_from_db()
    return {'msg': 'user has been deleted'}, 200
