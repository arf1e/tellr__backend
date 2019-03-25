from flask_restplus import Resource
from flask import request
from tellr.models.topic import TopicModel
from tellr.models.user import UserModel
from tellr.schemas.topic import TopicSchema

topic_schema = TopicSchema()
topic_list_schema = TopicSchema(many=True)


class Topic(Resource):
    def post(self):
        topic_json = request.get_json()
        topic = topic_schema.load(topic_json)
        topic.save_to_db()
        print(topic_schema.dump(topic))
        return {"msg": "sosat"}, 201

    def get(self):
        topics = TopicModel.find_all()
        return {"topics": topic_list_schema.dump(topics)}, 200
