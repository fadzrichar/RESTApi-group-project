import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required
from blueprints.faceplus.resources import GetKemiripan
from blueprints import internal_required

bp_mealdb = Blueprint('mealdb', __name__)
api = Api(bp_mealdb)

class Getmealdb(Resource):

    api_host = 'https://www.themealdb.com/api/json/v1/1'

    def __init__(self):
        pass

    @jwt_required
    # @internal_required
    def get(self):

        confidence = GetKemiripan().get()["confidence"]

        if confidence < 20 :
            menu = "a"
        elif confidence < 40 :
            menu = "b"
        elif confidence < 60 :
            menu = "c"
        elif confidence < 80 :
            menu = "d"
        else :
            menu = "e"

        # parser = reqparse.RequestParser()
        # parser.add_argument('f', location = 'args', default=None)
        # args = parser.parse_args()

        ## Step - 1 - check lon lat from ip
        rq = requests.get(self.api_host + '/search.php'+"?f="+menu)
        menus = rq.json()

        nama_meal = menus['meals'][0]['strMeal']
        img_meal = menus['meals'][0]['strMealThumb']

        return {
            'meals': {
                'Name'      : nama_meal,
                'Gambar'    : img_meal 
                }
            }

api.add_resource(Getmealdb, '')