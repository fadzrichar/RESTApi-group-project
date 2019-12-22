import requests, base64
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
import urllib.request as req
from blueprints.client.model import Clients
from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_instagram = Blueprint('instagram', __name__)
api = Api(bp_instagram)

class GetFotoandCaption(Resource):
    host = 'https://api.instagram.com/v1/users/self/media/recent/?access_token='
    # token = '1490266099.1677ed0.10681a6aa9274e388458e89d95ec7ffe'
    
    @jwt_required
    @internal_required
    def get(self):
        claim = get_jwt_claims()
        print(claim)
        token = claim['token_instagram']
        url = self.host+token+'&count=1'

        rq = requests.get(url)
        content = rq.json()
        foto = content['data'][0]['images']['standard_resolution']['url']
        caption = content['data'][0]['caption']['text']

        return {
            'foto' : foto,
            'caption' : caption
        }

class ConvertFoto(Resource):
    
    @jwt_required
    @internal_required
    def foto(self):
        instagram_foto = GetFotoandCaption().get()['foto']
        req.urlretrieve(instagram_foto, 'foto.jpg')

        with open('foto.jpg', 'rb') as imageFile:
            foto_byte = imageFile.read()
        return foto_byte


api.add_resource(GetFotoandCaption, '', '/<id>')
api.add_resource(ConvertFoto, '', '/<id>')