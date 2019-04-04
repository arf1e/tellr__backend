from flask_restplus import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

# models
from tellr.models.user import UserModel
from tellr.models.decision import DecisionModel

# schemas
from tellr.schemas.decision import DecisionSchema

decision_schema = DecisionSchema()
decision_list_schema = DecisionSchema(many=True)


class Decision(Resource):
    @classmethod
    @jwt_required
    def post(self, topic_id):
        user_id = get_jwt_identity()
        decision_json = request.get_json()
        decision_json["user_id"] = user_id
        decision_json["topic_id"] = topic_id
        decision = decision_schema.load(decision_json)
        decision.save_to_db()
        print(decision_schema.dump(decision))
        return {"msg": "sosat"}, 201
