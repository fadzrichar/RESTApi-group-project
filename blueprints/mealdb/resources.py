import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required

bp_mealdb = Blueprint('mealdb', __name__)
api = Api(bp_mealdb)

class Getmealdb(Resource):

    api_host = 'https://www.themealdb.com/api/json/v1/1'

    def __init__(self):
        pass
    
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('f', location = 'args', default=None)
        args = parser.parse_args()

        ## Step - 1 - check lon lat from ip
        rq = requests.get(self.api_host + '/search.php', params = {'f':args['f']})
        menu = rq.json()

        nama_meal = menu['meals'][0]['strMeal']
        img_meal = menu['meals'][0]['strMealThumb']

        return {
            'meals': {
                'Name'      : nama_meal,
                'Gambar'    : img_meal 
                }
            }

api.add_resource(Getmealdb, '/search.php')