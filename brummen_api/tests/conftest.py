# spin up the server
import pytest
from brummen_api.api import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

