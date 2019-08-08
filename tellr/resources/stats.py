from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from collections import Counter
from functools import reduce

from tellr.models.user import UserModel
from tellr.schemas.user import UserStatsSchema
from tellr.models.request import RequestModel
from tellr.schemas.request import RequestSchema


from tellr.models.badge import BadgeModel
from tellr.schemas.badge import BadgeSchema

badge_schema = BadgeSchema()
badge_list_schema = BadgeSchema(many=True)
user_schema = UserStatsSchema()


class Statistics(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        # that method is used to provide stats on how often other users assign certain badges to the user
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        user_json = user_schema.dump(user)
        # now we need to collect badges from user`s invoices and requests from other users in contacts
        request = "girl_request" if user_json["sex"] else "boy_request"
        invoices = user_json["invoices"]
        contacts = user_json["contacts"]
        total = len(invoices) + len(contacts)
        badges_list = []
        for invoice in invoices:
            badges_list.append(invoice["badges"])
        for contact in contacts:
            badges_list.append(contact[request]["badges"])
        if len(badges_list) == 0:
            return {"stats": [], "total": total}, 200
        # ok now we`re dealing with list which consists of two lists
        badges_list = reduce(lambda x, y: x + y, badges_list)  # flatten that boi
        stats = []
        for element in badges_list:
            stats.append(
                element["badge"]["id"]
            )  # it gives us list of badges ids [1,1,1,2,3,3,4]
        stats = Counter(stats)
        output = []
        for (
            _id,
            count,
        ) in stats.most_common():  # stats.most_common(): [(1, 3),(2,1),(3,2),(4,1)]
            output.append(
                {"badge": badge_schema.dump(BadgeModel.find_by_id(_id)), "times": count}
            )
        return {"stats": output, "total": total}, 200
