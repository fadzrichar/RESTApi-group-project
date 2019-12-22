# import json
# from . import client, create_token, reset_db
# from unittest import mock
# from unittest.mock import patch

# class TestMockMealdb():
# 	def mocked_requests_get(*args, **kwargs):
# 		class MockResponse:
# 			def __init__(self, json_data, status_code):
# 				self.json_data = json_data
# 				self.status_code = status_code

# 			def json(self):
# 				return self.json_data

# 		if len(args) > 0:
# 			if args[0] == "https://www.themealdb.com/api/json/v1/1/search.php?f=a":
# 				return MockResponse({
# 							"meals": [{
# 								"strMeal"       : "Ayam Geprek",
# 								"strMealThumb"  : "https://www.themealdb.com/images/media/meals/wyrqqq1468233628.jpg"
# 							}]
# 						}, 200)
# 		else:
# 			return MockResponse(None, 404)

# 	@mock.patch('requests.get', side_effect = mocked_requests_get)
# 	def test_meal(self, test_reqget_mock, client):

# 		res = client.get('/mealdb')
		
# 		assert res.status_code == 200