import pytest
import requests
from assign_3_test_endpoint import app as app_3


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
    

# POST
def test_post_new_clowder(client):
#curl -X POST -F "name=test2" -F "id=2" http://127.0.0.1:5000/
    test_data = {"name": "test", "id": "1"}
    response = client.post('/',data=test_data ,content_type='multipart/form-data')
 
    assert response.status_code == 201
    # test data in bucket and db match is below


'''def test_id_valid_get(client):
    response = client.get('/1')
    data = response.json()
    print (data)
    #assert data['Clowder_Information_DB'] == data['s3_data']

'''
# PUT with correct params

# PUT with incorrect params

# DELETE with correct params

# DELETE with incorrect params