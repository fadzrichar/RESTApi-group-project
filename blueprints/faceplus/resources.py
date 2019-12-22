import requests, shutil
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from blueprints.instagram.resources import GetFotoandCaption, ConvertFoto
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, jwt_required

bp_faceplus = Blueprint('faceplus', __name__)
api = Api(bp_faceplus)

class GetKemiripan(Resource):
    instagram_foto = ConvertFoto()
    instagram_foto = instagram_foto.foto()

    host = 'https://api-us.faceplusplus.com/facepp/v3/compare?'
    api_key = 'sDYn4R45akhLki48Uy5xVzdqdq9qMqqK'
    api_secret = '3jsLZXkF3HdBDEniCXCnjrOoL-ZfPuTe'
    image_url1 = 'https://cdn2.tstatic.net/manado/foto/bank/images/presiden-ri-jokowi-widodo_20180512_163325.jpg'
   

    url2 = host+'api_key='+api_key+'&api_secret='+api_secret+'&image_url1='+image_url1

    @jwt_required
    @internal_required
    def get(self):
        rq = requests.post(self.url2, files={'image_file2': self.instagram_foto})
        content = rq.json()
        confidence = content["confidence"]

        return {
            'confidence' : confidence
        }

api.add_resource(GetKemiripan, '')
        