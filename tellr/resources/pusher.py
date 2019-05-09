from flask_restplus import Resource
from flask import request
from tellr.pusher import pusher_client


class PusherAuth(Resource):
    @classmethod
    def post(cls):
        auth = pusher_client.authenticate(
            channel=request.form["channel_name"], socket_id=request.form["socket_id"]
        )
        return {"auth": auth["auth"]}, 200
