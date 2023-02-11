import pytest
import datetime
from starlette.testclient import TestClient
from api.fastapi_app import create_app


@pytest.fixture()
def client():
    with TestClient(create_app()) as client:
        yield client


def test_hello_world(client):
    response = client.get("/hello_world")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_parrot_back(client):
    post_json = {
        "header": "my_header",
        "parrot_request": {
            "n_repeat": 3,
            "sep": ", ",
            "parrot_str": "blah"
        }
    }
    response = client.post("/parrot_back", json=post_json)
    assert response.status_code == 200
    j = response.json()
    assert j["header"] == "my_header"
    assert j["results"]["parrot"] == "parrot back blah, blah, blah"
    datetime.datetime.strptime(j["results"]["time"], "%Y-%m-%dT%H:%M:%SZ")
