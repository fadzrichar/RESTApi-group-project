import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required
from blueprints.instagram.resources import GetFotoandCaption
from blueprints.paralleldot.resources import PostImgRecognizer
from blueprints.faceplus.resources import GetKemiripan
from blueprints.mealdb.resources import Getmealdb


bp_promo = Blueprint('promo', __name__)
api = Api(bp_promo)

class Promotion(Resource):
    score = PostImgRecognizer().post()['score']
    caption = GetFotoandCaption().get()['caption']
    foodname = Getmealdb().get()['meals']['Name']
    pict = Getmealdb().get()['meals']['Gambar']
    
    def get(self):
        words = self.caption.split(' ')
        if 'Jokowi' in words and 'HAPPY' in words and 'BIRTHDAY' in words:
            if self.score > 0.8:
                return {
                    'Makanan'   :self.foodname,
                    'Diskon'    :'50%',
                    'Gambar'    :self.pict
                }
            elif self.score > 0.5:
                return {
                    'Makanan'   :self.foodname,
                    'Diskon'    :'30%',
                    'Gambar'    :self.pict
                }
            elif self.score > 0.2:
                return {
                    'Makanan'   :self.foodname,
                    'Diskon'    :'20%',
                    'Gambar'    :self.pict
                }
            elif self.score > 0:
                return {
                    'Makanan'   :self.foodname,
                    'Diskon'    :'10%',
                    'Gambar'    :self.pict
                }
            else:
                return "Maaf, gambar yang anda post tidak memenuhi kebetuhan"
        else:
            return "Caption tidak memenuhi ketentuan"

api.add_resource(Promotion,'')