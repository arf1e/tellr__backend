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
from tellr.models.contact import ContactModel
from tellr.models.guess import GuessModel

# schemas
from tellr.schemas.user import UserSchema
from tellr.schemas.answer import AnswerSchema
from tellr.schemas.request import RequestSchema, GuessSchema
from tellr.schemas.contact import ContactSchema

# stuff
from tellr.blacklist import BLACKLIST
from tellr.libs.passwords import encrypt_password, check_encrypted_password
from tellr.db import db


user_schema = UserSchema()
user_list_schema = UserSchema(many=True)
answer_schema = AnswerSchema()
answer_list_schema = AnswerSchema(many=True)
request_schema = RequestSchema()
contact_schema = ContactSchema()
contact_list_schema = ContactSchema(many=True)
guess_schema = GuessSchema()
guess_list_schema = GuessSchema(many=True)

DATABASE_ERROR = "Database error"


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

        try:
            user.save_to_db()
        except:
            return {"message": DATABASE_ERROR}, 500
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
        if duplicate:
            return {"message": "request exists"}, 200
        req_input = request.get_json()
        req_input["asker_id"] = asker_id
        req_input["receiver_id"] = user_id
        guesses_json = req_input.pop("guesses", None)
        print(req_input)
        req = request_schema.load(req_input)
        match = RequestModel.find_existing(user_id, asker_id)
        if match:
            match.accepted = True
            req.accepted = True
            try:
                match.save_to_db()
            except:
                return {"message": DATABASE_ERROR}, 500
        req.save_to_db()
        for guess in guesses_json:
            guess["request_id"] = req.id
            guess_schema.load(guess).save_to_db()
        if match:
            if user.sex == False:
                contact = contact_schema.load(
                    {
                        "boy_id": asker_id,
                        "girl_id": user_id,
                        "boy_request": req.id,
                        "girl_request": match.id,
                    }
                )
                try:
                    contact.save_to_db()
                except:
                    return {"message": DATABASE_ERROR}, 500
                return {"message": "contact created"}, 201
            else:
                contact = contact_schema.load(
                    {
                        "boy_id": user_id,
                        "girl_id": asker_id,
                        "boy_request": match.id,
                        "girl_request": req.id,
                    }
                )
                try:
                    contact.save_to_db()
                except:
                    return {"message": DATABASE_ERROR}, 500
                return {"message": "contact created"}, 200
        return {"request": request_schema.dump(req)}, 201
        # =========================================
        # request_input = request.get_json()
        # request_input["asker_id"] = asker_id
        # request_input["receiver_id"] = user_id
        # req = request_schema.load(request_input)
        # if match:
        #     req.accepted = True
        #     try:
        #         req.save_to_db()
        #     except:
        #         return {"message": DATABASE_ERROR}, 500
        #     print(req)
        #     match.accepted = True
        #     if user.sex == False:
        #         contact = contact_schema.load(
        #             {
        #                 "boy_id": asker_id,
        #                 "girl_id": user_id,
        #                 "boy_request": req.id,
        #                 "girl_request": match.id,
        #             }
        #         )
        #         try:
        #             contact.save_to_db()
        #         except:
        #             return {"message": DATABASE_ERROR}, 500
        #     try:
        #         match.save_to_db()
        #     except:
        #         return {"message": DATABASE_ERROR}, 500
        #     return {"msg": "friend request"}, 200
        # try:
        #     req.save_to_db()
        # except:
        #     return {"message": DATABASE_ERROR}, 500
        # return {"request": request_schema.dump(req)}, 201


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        print(get_raw_jwt()["jti"])
        jti = get_raw_jwt()["jti"]
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
        friends = []
        print(user["outvoices"] + friends)
        for contact in user["contacts"]:
            if user["sex"] == True:
                friends.append(contact["girl_id"])
            else:
                friends.append(contact["boy_id"])
        if user["sex"] == True:
            users = user_list_schema.dump(
                UserModel.find_females(user["outvoices"] + friends)
            )
        else:
            users = user_list_schema.dump(
                UserModel.find_males(user["outvoices"] + friends)
            )
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
