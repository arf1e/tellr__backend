from flask_restplus import Resource
from flask import request
from tellr.models.topic import TopicModel
from tellr.models.user import UserModel

from tellr.schemas.topic import TopicSchema
from tellr.schemas.user import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

topic_schema = TopicSchema()
topic_list_schema = TopicSchema(many=True)
user_schema = UserSchema()


class Topic(Resource):
    def post(self):
        topic_json = request.get_json()
        topic = topic_schema.load(topic_json)
        topic.save_to_db()
        print(topic_schema.dump(topic))
        return {"msg": "sosat"}, 201

    @classmethod
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        user_dict = user_schema.dump(user)
        total = user_dict["hated"] + user_dict["loved"]
        topic = TopicModel.get_topics(total)
        return topic_list_schema.dump(topic), 200
