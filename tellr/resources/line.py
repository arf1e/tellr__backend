from flask_restplus import Resource
from flask import request
from tellr.schemas.line import LineSchema
from tellr.models.line import LineModel
from flask_jwt_extended import jwt_required, get_jwt_identity

line_schema = LineSchema()
lines_list_schema = LineSchema(many=True)


class Line(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        line_json = request.get_json()
        user_id = get_jwt_identity()
        line = line_schema.load({"user_id": user_id, **line_json})
        try:
            line.save_to_db()
        except:
            return {"message": "Server Error"}, 500
        return line_schema.dump(line), 201


class Lines(Resource):
    @classmethod
    def get(cls):
        lines = lines_list_schema.dump(LineModel.get_lines())
        return {"lines": lines}
