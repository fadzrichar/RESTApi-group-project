import json
from . import client, create_token, reset_db

class TestClientCrud():

    idPerson = 0
    reset_db()

    # ======================================= POST ==================================== #

    def test_client_post_internal(self, client):
        token = create_token(True)

        data = {
            "client_key": "CLIENT02",
            "client_secret": "SECRET02",
            "status":True
        }

        res = client.post('/client', query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0
        # assert res_json['client_secret'] == hashlib.md5(data['client_secret'])
        
        self.idPerson = res_json['id']

    # ======================================= GET ==================================== #

    def test_client_get_id_internal(self, client):
        token = create_token(True)
        res = client.get('/client/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_client_get_id_internal_id_outrange(self, client):
        token = create_token(True)
        res = client.get('/client/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404

    # ======================================= PUT ==================================== #

    def test_client_put_internal(self, client):
        token = create_token(True)

        data = {
            "client_key": "CLIENT02",
            "client_secret": "SECRET02",
            "status": False
        }

        res = client.put('/client/2', query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0
        # assert res_json['client_secret'] == hashlib.md5(data['client_secret'])
        
        self.idPerson = res_json['id']

    def test_client_put_internal_id_notfound(self, client):
        token = create_token(True)

        data = {
            "client_key": "CLIENT02",
            "client_secret": "SECRET02",
            "status": True
        }

        res = client.put('/client/100', query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    def test_client_put_noninternal(self, client):
        token = create_token(False)

        data = {
            "client_key": "CLIENT02",
            "client_secret": "SECRET02",
            "status": True
        }

        res = client.put('/client/1', query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 403
        # assert res_json['client_secret'] == hashlib.md5(data['client_secret'])
        
    
    # ======================================= GET_All ==================================== #

    def test_client_get_all_internal_clientid_True(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "client_id":1,
            "sort":"desc"
        }

        res = client.get('/client', query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_client_get_all_internal_sortby_status_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "client_id":1,
            "orderby":"status",
            "sort":"desc"
        }

        res = client.get('/client', query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_client_get_all_internal_sortby_status_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "client_id":1,
            "status":True,
            "orderby":"status",
            "sort":"asc"
        }

        res = client.get('/client', query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    # ======================================= DELETE ==================================== #

    def test_client_delete_id_internal(self, client):
        token = create_token(True)
        res = client.delete('/client/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_client_delete_id_internal_idnotfound(self, client):
        token = create_token(True)
        res = client.delete('/client/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 404

    # ======================================= PATCH ==================================== #

    def test_client_patch_internal(self, client):
        token = create_token(True)
        res = client.patch('/client',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 501