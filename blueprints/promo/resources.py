import requests
from flask import Blueprint
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import jwt_required
from blueprints.instagram.resources import GetFotoandCaption
from blueprints.paralleldot.resources import PostImgRecognizer
from blueprints.faceplus.resources import GetKemiripan
from blueprints.mealdb.resources import Getmealdb
from blueprints import internal_required



bp_promo = Blueprint('promo', __name__)
api = Api(bp_promo)

class Promotion(Resource):

    @jwt_required
    def get(self):
        score = PostImgRecognizer().post()['score']
        caption = GetFotoandCaption().get()['caption']
        foodname = Getmealdb().get()['meals']['Name']
        pict = Getmealdb().get()['meals']['Gambar']
        words = caption.split(' ')
        lowerword=[]
        for data in words:
            kecil = data.lower()
            lowerword.append(kecil)

        if 'jokowi' in lowerword and 'happy' in lowerword and 'birthday' in lowerword:
            if score > 0.8:
                return {
                    'Makanan'   :foodname,
                    'Diskon'    :'50%',
                    'Gambar'    :pict
                }, 200
            elif score > 0.5:
                return {
                    'Makanan'   :foodname,
                    'Diskon'    :'30%',
                    'Gambar'    :pict
                }, 200
            elif score > 0.2:
                return {
                    'Makanan'   :foodname,
                    'Diskon'    :'20%',
                    'Gambar'    :pict
                }, 200
            elif score > 0:
                return {
                    'Makanan'   :foodname,
                    'Diskon'    :'10%',
                    'Gambar'    :pict
                }, 200
            else:
                return {'message':"Maaf, gambar yang anda post tidak memenuhi ketentuan(Tidak terdapat gambar makanan)"}, 404
        else:
            return {'message' : "Caption tidak memenuhi ketentuan"}, 404
          
    
api.add_resource(Promotion,'')