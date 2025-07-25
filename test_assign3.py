import pytest
from assign_3 import app as app_3

@pytest.fixture()
def app():
    app = app_3
    app.config.update({
        "TESTING": True,
    })
    yield app  

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_empty_get(client):
    response = client.get('/')
    assert response.status_code == 200

def test_no_data_get(client):
    response = client.get('/0')
    assert response.status_code == 401
    
def test_wrong_id_get(client):
    response = client.get('/a')
    assert response.status_code == 400
    
def test_post_new_clowder(client):
    test_data = {"name": "test", "id": "1"}
    response = client.post('/',data=test_data ,content_type='multipart/form-data')
 
    assert response.status_code == 201
    # test data in bucket and db match is below

def test_id_valid_get(client):
    response = client.get('/1')
    response_dict = response.json
    assert response.status_code == 201
    assert response_dict['Clowder_Information_DB'] == response_dict['s3_data']

def test_valid_put(client):
    response = client.put('update/1',json ={"Clowder_Name": "new_name", "cat_info":{"cat_name":"Baxter","gender":"male"}})
    response_dict = response.json
    assert response.status_code == 202
    assert response_dict['New_Clowder_info'] == response_dict['s3_data']
    
def test_bad_id_put(client):
    response = client.put('update/0',json ={"Clowder_Name": "new_name", "cat_info":{"cat_name":"Baxter","gender":"male"}})
    assert response.status_code == 404

def test_valid_delete(client):
    response = client.delete('delete/1')
    response_dict = response.json
    assert response.status_code == 202
    assert response_dict['Deleted_Clowder_Info_DB']['Clowder_Id'] == response_dict['Deleted_Clowder_Info_s3'][0]['Key']
    
def test_bad_id_delete(client):
    response = client.delete('delete/1')
    response_dict = response.json
    assert response.status_code == 404