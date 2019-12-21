import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from blueprints.instagram.resources import GetFotoandCaption

bp_faceplus = Blueprint('faceplus', __name__)
api = Api(bp_faceplus)

class GetKemiripan(Resource):
    instagram_data = GetFotoandCaption()

    host = 'https://api-us.faceplusplus.com/facepp/v3/compare?'
    api_key = 'sDYn4R45akhLki48Uy5xVzdqdq9qMqqK'
    api_secret = '3jsLZXkF3HdBDEniCXCnjrOoL-ZfPuTe'
    image_url1 = 'https://cdn2.tstatic.net/manado/foto/bank/images/presiden-ri-jokowi-widodo_20180512_163325.jpg'
    # image_url2 = instagram_data.get()['foto']
    image_url2 = 'https://mmc.tirto.id/image/otf/500x0/2019/11/11/antarafoto-rapat-menhan-dengan-dpr-111119-app-14_ratio-16x9.jpg'
    # image_url2 = 'https://scontent.cdninstagram.com/v/t51.2885-15/sh0.08/e35/s640x640/66391286_2294013900705901_4376247166940848407_n.jpg?_nc_ht=scontent.cdninstagram.com&_nc_ohc=lgXLtbNOIWcAX9jezE1&oh=fc072ffe40c35123812215871383404e&oe=5EA9E951'

    url = host+'api_key='+api_key+'&api_secret='+api_secret+'&image_url1='+image_url1+'&image_url2='+image_url2

    def get(self):
        rq = requests.post(self.url)
        content = rq.json()
        confidence = content["confidence"]

        return {
            'confidence' : confidence
        }

api.add_resource(GetKemiripan, '')
        