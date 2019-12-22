import json
from . import client, create_token, reset_db
from unittest import mock
from unittest.mock import patch
from blueprints.instagram.resources import GetFotoandCaption
from blueprints.paralleldot.resources import PostImgRecognizer
from blueprints.faceplus.resources import GetKemiripan
from blueprints.mealdb.resources import Getmealdb
from blueprints import internal_required

class TestMockPromo():
	def mocked_requests_get(*args, **kwargs):
		class MockResponse():
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data
		
		if len(args)>0:
			if args[0] == "https://api.instagram.com/v1/users/self/media/recent/?access_token=18098825952.1677ed0.82f8795bed2a455397ededddbcdd66ca&count=1":
				return MockResponse({
			'data':[
				{
				'images' :
					{
					'standard_resolution' : 
						{
						'url' : "https://scontent.cdninstagram.com/v/t51.2885-15/e35/72973108_2861605547223250_1462930368002669093_n.jpg?_nc_ht=scontent.cdninstagram.com&_nc_ohc=NIOEvEO5NVUAX-8H0rA&oh=394ce4a512ca06370a940418d5962ba7&oe=5E9895E7"
						}
					},
				'caption' : 
					{
						'text' : 'Happy Birthday Pakde Jokowi'
					}
				}
			]
			}, 200)

			if args[0] == "https://apis.paralleldots.com/v4/object_recognizer":
				return MockResponse({
				"output": [
						{
							"tag": "Food",
							"score": 0.3
						}
					]
				}, 200)

			elif args[0] == "https://www.themealdb.com/api/json/v1/1/search.php?f=a":
				return MockResponse({
							"meals": [{
								"strMeal"       : "Ayam Geprek",
								"strMealThumb"  : "https://www.themealdb.com/images/media/meals/wyrqqq1468233628.jpg"
							}]
						}, 200)
			elif args[0] == "https://www.themealdb.com/api/json/v1/1/search.php?f=b":
				return MockResponse({
							"meals": [{
								"strMeal"       : "Ayam Geprek",
								"strMealThumb"  : "https://www.themealdb.com/images/media/meals/wyrqqq1468233628.jpg"
							}]
						}, 200)
			elif args[0] == "https://www.themealdb.com/api/json/v1/1/search.php?f=c":
				return MockResponse({
							"meals": [{
								"strMeal"       : "Ayam Geprek",
								"strMealThumb"  : "https://www.themealdb.com/images/media/meals/wyrqqq1468233628.jpg"
							}]
						}, 200)
			elif args[0] == "https://www.themealdb.com/api/json/v1/1/search.php?f=d":
				return MockResponse({
							"meals": [{
								"strMeal"       : "Ayam Geprek",
								"strMealThumb"  : "https://www.themealdb.com/images/media/meals/wyrqqq1468233628.jpg"
							}]
						}, 200)
			elif args[0] == "https://www.themealdb.com/api/json/v1/1/search.php?f=e":
				return MockResponse({
							"meals": [{
								"strMeal"       : "Ayam Geprek",
								"strMealThumb"  : "https://www.themealdb.com/images/media/meals/wyrqqq1468233628.jpg"
							}]
						}, 200)
			
			else:
				return MockResponse(None, 404)

	def mocked_requestskemiripana_get(*args, **kwargs):
		class MockResponse():
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data
		var1={"confidence":15}
		return var1
	
	def mocked_requestskemiripanb_get(*args, **kwargs):
		class MockResponse():
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data
		var1={"confidence":25}
		return var1

	def mocked_requestskemiripanc_get(*args, **kwargs):
		class MockResponse():
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data
		var1={"confidence":55}
		return var1
	
	def mocked_requestskemiripand_get(*args, **kwargs):
		class MockResponse():
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data
		var1={"confidence":75}
		return var1
	
	def mocked_requestskemiripane_get(*args, **kwargs):
		class MockResponse():
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data
		var1={"confidence":95}
		return var1
	
	def mocked_requests_post(*args, **kwargs):
		class MockResponse:
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data

		if len(args) > 0:
			if args[0] == "https://apis.paralleldots.com/v4/object_recognizer":
				return MockResponse({
				"output": [
						{
							"tag": "Food",
							"score": 0.3
						}
					]
				}, 200)
		else:
			return MockResponse(None, 404)
			   
	# @mock.patch('requests.post',side_effect=mocked_requests_post)	
	# @mock.patch.object(GetKemiripan,"get", side_effect=mocked_requestskemiripanb_get)
	@mock.patch('requests.get',side_effect=mocked_requests_get)
	def test_promo(self, test_req_mock, client):
		token = create_token(True)

		res = client.get('/promo',
		headers={'Authorization': 'Bearer ' + token})
		assert res.status_code == 200
	