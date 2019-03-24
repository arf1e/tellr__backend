from flask_restplus import Resource
from flask import request
from tellr.schemas.line import LineSchema
from tellr.models.line import LineModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from tellr.models.user import UserModel
from tellr.schemas.user import UserSchema

user_schema = UserSchema()
line_schema = LineSchema()
lines_list_schema = LineSchema(many=True)


class LineCreate(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        line_json = request.get_json()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        user_json = user_schema.dump(user)
        if len(user_json["lines"]) >= 3:
            return {"message": "max lines amount reached"}, 204
        line = line_schema.load({"user_id": user_id, **line_json})
        try:
            line.save_to_db()
        except:
            return {"message": "Server Error"}, 500
        return line_schema.dump(line), 201


class Line(Resource):
    @classmethod
    @jwt_required
    def delete(cls, line_id):
        line = LineModel.find_by_id(line_id)
        user_id = get_jwt_identity()
        line_json = line_schema.dump(line)
        if line_json["user_id"] == user_id:
            line.delete_from_db()
            user = UserModel.find_by_id(user_id)
            return {"lines": lines_list_schema.dump(user.lines)}, 200
        return {"message": "Unauthorized"}, 401

    @classmethod
    def get(cls, line_id):
        line = LineModel.find_by_id(id)
        if line:
            return {"line": line_schema.dump(line)}, 200
        return {"message": "line was not found"}, 404

    @classmethod
    @jwt_required
    def patch(cls, line_id):
        line = LineModel.find_by_id(line_id)
        user_id = get_jwt_identity()
        updated = request.get_json()
        if line and line.user_id == user_id:
            line.correct_id = updated["correct_id"]
            line.save_to_db()
            user = UserModel.find_by_id(user_id)
            return {"lines": lines_list_schema.dump(user.lines)}, 200
        return {"message": "Line was not found on this user"}, 404


class Lines(Resource):
    @classmethod
    def get(cls):
        lines = lines_list_schema.dump(LineModel.get_lines())
        return {"lines": lines}
