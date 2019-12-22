import json
from . import client, create_token, reset_db
from unittest import mock
from unittest.mock import patch
from blueprints.faceplus.resources import GetKemiripan

class TestMockMealdb():
	def mocked_requests_get(*args, **kwargs):
		class MockResponse():
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data

		if len(args) > 0:
			if args[0] == "https://www.themealdb.com/api/json/v1/1/search.php?f=a":
				return MockResponse({
							"meals": [{
								"strMeal"       : "Ayam Geprek",
								"strMealThumb"  : "https://www.themealdb.com/images/media/meals/wyrqqq1468233628.jpg"
							}]
						}, 200)
			if args[0] == "https://www.themealdb.com/api/json/v1/1/search.php?f=b":
				return MockResponse({
							"meals": [{
								"strMeal"       : "Ayam Geprek",
								"strMealThumb"  : "https://www.themealdb.com/images/media/meals/wyrqqq1468233628.jpg"
							}]
						}, 200)
			if args[0] == "https://www.themealdb.com/api/json/v1/1/search.php?f=c":
				return MockResponse({
							"meals": [{
								"strMeal"       : "Ayam Geprek",
								"strMealThumb"  : "https://www.themealdb.com/images/media/meals/wyrqqq1468233628.jpg"
							}]
						}, 200)
			if args[0] == "https://www.themealdb.com/api/json/v1/1/search.php?f=d":
				return MockResponse({
							"meals": [{
								"strMeal"       : "Ayam Geprek",
								"strMealThumb"  : "https://www.themealdb.com/images/media/meals/wyrqqq1468233628.jpg"
							}]
						}, 200)
			if args[0] == "https://www.themealdb.com/api/json/v1/1/search.php?f=e":
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


	@mock.patch.object(GetKemiripan,"get", side_effect=mocked_requestskemiripanb_get)
	@mock.patch('requests.get', side_effect = mocked_requests_get)
	def test_mealb(self, test_reqget_mock, test_reqgetkem_mock, client):
		token = create_token(True)

		res = client.get('/mealdb',headers={'Authorization': 'Bearer ' + token})
		assert res.status_code == 200

	@mock.patch.object(GetKemiripan,"get", side_effect=mocked_requestskemiripana_get)
	@mock.patch('requests.get', side_effect = mocked_requests_get)
	def test_meala(self, test_reqget_mock, test_reqgetkem_mock, client):
		token = create_token(True)

		res = client.get('/mealdb',headers={'Authorization': 'Bearer ' + token})
		assert res.status_code == 200
	
	@mock.patch.object(GetKemiripan,"get", side_effect=mocked_requestskemiripanc_get)
	@mock.patch('requests.get', side_effect = mocked_requests_get)
	def test_mealc(self, test_reqget_mock, test_reqgetkem_mock, client):
		token = create_token(True)

		res = client.get('/mealdb',headers={'Authorization': 'Bearer ' + token})
		assert res.status_code == 200

	@mock.patch.object(GetKemiripan,"get", side_effect=mocked_requestskemiripand_get)
	@mock.patch('requests.get', side_effect = mocked_requests_get)
	def test_meald(self, test_reqget_mock, test_reqgetkem_mock, client):
		token = create_token(True)

		res = client.get('/mealdb',headers={'Authorization': 'Bearer ' + token})
		assert res.status_code == 200

	@mock.patch.object(GetKemiripan,"get", side_effect=mocked_requestskemiripane_get)
	@mock.patch('requests.get', side_effect = mocked_requests_get)
	def test_meale(self, test_reqget_mock, test_reqgetkem_mock, client):
		token = create_token(True)

		res = client.get('/mealdb',headers={'Authorization': 'Bearer ' + token})
		assert res.status_code == 200