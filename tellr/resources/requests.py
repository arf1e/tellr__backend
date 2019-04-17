from flask_restplus import Resource
from tellr.models.request import RequestModel
from tellr.schemas.request import RequestSchema

request_list_schema = RequestSchema(many=True)


class Requests(Resource):
    @classmethod
    def get(cls):
        requests = RequestModel.find_all()
        return {"requests": request_list_schema.dump(requests)}, 200


class Request(Resource):
    @classmethod
    def delete(cls, req_id):
        request = RequestModel.find_by_id(req_id)
        if request:
            request.delete_from_db()
            return {"message": "request was deleted"}, 200
        return {"message": "request was not found"}, 404
