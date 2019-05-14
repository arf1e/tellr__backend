from flask_restplus import Resource
from flask import request
from tellr.schemas.badge import BadgeSchema
from tellr.models.badge import BadgeModel

badge_schema = BadgeSchema()
badge_list_schema = BadgeSchema(many=True)


class Badge(Resource):
    def post(self):
        badge_json = request.get_json()
        badge = badge_schema.load(badge_json)
        try:
            badge.save_to_db()
        except:
            return {"msg": "Server error"}, 500
        badge_entity = badge_schema.dump(badge)
        return {"badge": badge_entity}, 201
