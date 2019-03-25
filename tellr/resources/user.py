# libs
from datetime import date, datetime
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

# models
from tellr.models.user import UserModel
from tellr.models.answer import AnswerModel
from tellr.models.request import RequestModel

# schemas
from tellr.schemas.user import UserSchema
from tellr.schemas.answer import AnswerSchema
from tellr.schemas.request import RequestSchema

# stuff
from tellr.blacklist import BLACKLIST
from tellr.libs.passwords import encrypt_password, check_encrypted_password


user_schema = UserSchema()
user_list_schema = UserSchema(many=True)
answer_schema = AnswerSchema()
answer_list_schema = AnswerSchema(many=True)
request_schema = RequestSchema()


class UserRegister(Resource):
    def post(self):

        user_json = request.get_json()
        if "birthday" in user_json:
            bday = user_json["birthday"].split("-")
            user_json["birthday"] = f"{bday[2]}-{bday[1]}-{bday[0]}T00:00:00Z"
            user_json["password"] = encrypt_password(user_json["password"])
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
        if user and check_encrypted_password(user_json["password"], user.password):
            access_token = create_access_token(identity=user.id, expires_delta=False)
            refresh_token = create_refresh_token(user.id)
            return (
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user_schema.dump(user),
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
        user_output = user_schema.dump(user)
        for line in user_output["lines"]:
            line["answers"] = answer_list_schema.dump(
                AnswerModel.get_wrong_answers(
                    question_id=line["question_id"], correct_id=line["correct"]["id"]
                )
            )
        return user_output, 200

    # @classmethod
    # def delete(cls, user_id):
    #     user = UserModel.find_by_id(user_id)
    #     if not user:
    #         return {"msg": "user not found"}, 404
    #     user.delete_from_db()
    #     return {"msg": "user has been deleted"}, 200

    @classmethod
    @jwt_required
    def post(cls, user_id):
        user = UserModel.find_by_id(user_id)
        asker_id = get_jwt_identity()
        duplicate = RequestModel.find_existing(asker_id, user_id)
        request_input = request.get_json()
        request_input["asker_id"] = asker_id
        request_input["receiver_id"] = user_id
        req = request_schema.load(request_input)
        req.save_to_db()
        return {"request": request_schema.dump(req)}, 200


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        print(get_raw_jwt()["jti"])
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", unique identifier for JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": f"User <id={user_id}> has logged out"}, 200


# Поиск
class UserQuery(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        user_data = UserModel.find_by_id(user_id)
        user = user_schema.dump(user_data)
        if user["sex"] == True:
            users = user_list_schema.dump(UserModel.find_females())
        else:
            users = user_list_schema.dump(UserModel.find_males())
        for user in users:
            for line in user["lines"]:
                # [users].len is always 4, so O(n^2) here is no big deal
                line["answers"] = answer_list_schema.dump(
                    AnswerModel.get_wrong_answers(
                        question_id=line["question_id"],
                        correct_id=line["correct"]["id"],
                    )
                )
        return {"users": users}, 200
