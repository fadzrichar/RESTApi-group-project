import json
from . import client, create_token, reset_db
from unittest import mock
from unittest.mock import patch

class TestMockParalleldot():
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

	@mock.patch('requests.post',side_effect=mocked_requests_post)
	def test_paralleldot(self, test_reqget_mock, client):
		token = create_token(True)

		# data ={
		# 		"output": [
		# 				{
		# 					"tag": "Food",
		# 					"score": 0.3
		# 				}
		# 			]
		# 		}
		res = client.post('/imgrecognizer',
		headers={'Authorization': 'Bearer ' + token})

		res_json = json.loads(res.data)

		assert res.status_code == 200