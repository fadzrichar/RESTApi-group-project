import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource

bp_instagram = Blueprint('instagram', __name__)
api = Api(bp_instagram)

class GetFotoandCaption(Resource):
    host = 'https://api.instagram.com/v1/users/self/media/recent/?access_token=1490266099.1677ed0.10681a6aa9274e388458e89d95ec7ffe&count=1'

    def get(self):
        rq = requests.get(self.host)
        content = rq.json()
        foto = content['data'][0]['images']['standard_resolution']['url']
        caption = content['data'][0]['caption']['text']

        return {
            'foto' : foto,
            'caption' : caption
        }

api.add_resource(GetFotoandCaption, '')