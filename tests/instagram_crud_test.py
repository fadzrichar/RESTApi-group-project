import json
from . import *
from unittest import mock
from unittest.mock import patch

class TestMockInstagram():
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            
            def json(self):
                return self.json_data
        
        return MockResponse(
        {
            'data':
            [
                {
                'images' :
                    {
                    'standard_resolution' : 
                        {
                        'url' : 'ini url untuk dapet foto instagram'
                        }
                    },
                'caption' : 
                    {
                    'text' : 'ini text untuk caption'
                    }
                }
            ]
        })

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_instagram(self, test_reqget_mock, client):
        token = create_token()

        res = client.get('instagram', headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
            