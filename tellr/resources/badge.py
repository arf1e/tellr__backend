from flask_restplus import Resource
from flask import request
from tellr.schemas.badge import BadgeSchema
from tellr.models.badge import BadgeModel

badge_schema = BadgeSchema()
badge_list_schema = BadgeSchema(many=True)


class Badge(Resource):
    def get(self, badge_id):
        badge = BadgeModel.find_by_id(badge_id)
        if badge:
            return {"badge": badge_schema.dump(badge)}, 200
        return {"msg": "No badge with such id"}

    def post(self):
        badge_json = request.get_json()
        badge = badge_schema.load(badge_json)
        try:
            badge.save_to_db()
        except:
            return {"msg": "Server error"}, 500
        badge_entity = badge_schema.dump(badge)
        return {"badge": badge_entity}, 201

    def delete(self, badge_id):
        badge = BadgeModel.find_by_id(badge_id)
        if badge:
            try:
                badge.delete_from_db()
            except:
                return {"msg": "Server error"}, 500
            return {"msg": "badge deleted"}, 200
        else:
            return {"msg": "no badge with such id"}, 404


class BadgeList(Resource):
    @classmethod
    def get(cls):
        badges = BadgeModel.find_all()
        return {"badges": badge_list_schema.dump(badges)}, 200
