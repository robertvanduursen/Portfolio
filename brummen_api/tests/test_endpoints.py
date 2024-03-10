# run the tests on the endpoint

def test_index(client):
    # proof the func
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Python API demo' in response.data

