import pytest, json, logging
from blueprints import app, db
from app import cache
from flask import Flask, request

from blueprints.client.model import Clients

def reset_db():
    db.drop_all()
    db.create_all()

    data_client = Clients("CLIENT01", "c1955d22ee05fe485b17369342225129", True, '18098825952.1677ed0.82f8795bed2a455397ededddbcdd66ca')
    db.session.add(data_client)
    db.session.commit()
    data_client = Clients("internal", "24f8581e79dde8c0f1768968accbca28", True, '18098825952.1677ed0.82f8795bed2a455397ededddbcdd66ca')
    db.session.add(data_client)
    db.session.commit()
    
def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token(isinternal=False):
    if isinternal:
        cachename = 'test-internal-token'
        data = {
            "client_key":"internal",
            "client_secret":"internal123"
        }
    else:
        cachename = 'test-token'
        data = {
            "client_key":"CLIENT01",
            "client_secret":"SECRET01"
        }

    token = cache.get(cachename)

    if token is None:
        # Do request
        req = call_client(request)
        res = req.get('/token',query_string = data)

        # Store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        # assert / compare with expected result
        assert res.status_code == 200

        # save token into cache
        cache.set(cachename, res_json['token'], timeout = 60)

        # return, because it usefull for other test
        return res_json['token']
    
    else:
        return token
