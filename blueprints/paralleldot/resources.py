import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required

bp_paralleldot = Blueprint('paralleldot', __name__)
api = Api(bp_paralleldot)

class PostImgRecognizer(Resource):
    parallel_host = 'https://apis.paralleldots.com/v4/object_recognizer'
    parallel_apikey = 'm6GGf7N7VXvUejnSd8XP0NUzq8KRyxkgZCm2Nz730Vg'

    # @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', location='json', default=None)
        # parser.add_argument('api_key', location='json', default=None)
        args = parser.parse_args()

        ## step - 1 - check
        data = requests.post(self.parallel_host, data={ "api_key": self.parallel_apikey ,"url":args['url']})
        datajson = data.json()
        datajson = datajson['output']
        for data in datajson:
            if data['tag'] == 'Food':
                return data
        return "SORRY, NO FOOD DETECTED!!!!"

api.add_resource(PostImgRecognizer,'')