import pytest, logging, hashlib
from flask import Flask, request, json
from blueprints import app, db
from app import app, cache
from blueprints.client.model import Clients

def reset_db():
    db.drop_all()
    db.create_all()

    client = Clients("internal",hashlib.md5("th1s1s1nt3n4lcl13nt".encode()).hexdigest(),True)
    db.session.add(client)
    db.session.commit()

    client = Clients("CLIENT01",hashlib.md5("SECRET01".encode()).hexdigest(),False)
    db.session.add(client)
    db.session.commit()


def call_client(request):
    client = app.test_client()
    return client
    
@pytest.fixture
def client(request):
    return call_client(request)

def create_token(isInternal=False):
    if isInternal:
        cachename = 'test-internal-token'
        data = {
            "client_key":"internal",
            "client_secret":"th1s1s1nt3n4lcl13nt"
        }
    else:
        cachename = 'test-token'
        data = {
            'client_key':'CLIENT01',
            'client_secret':'SECRET01'
        }
    token = cache.get(cachename)
    # prepare request input
    
    if token is None:
        # do request
        req = call_client(request)
        res = req.get('/token',
                        query_string=data)

        # store respons
        res_json = json.loads(res.data)

        logging.warning('RESULT: %s', res_json)

        # assert / compare with expected result
        assert res.status_code == 200

        # save token into cache
        cache.set(cachename, res_json['token'], timeout=60)

        # return, bcz it usefull for other test
        return res_json['token']
    else:
        return token