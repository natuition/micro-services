from app.main import app
from fastapi.testclient import TestClient
import pytest


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def delete_all_data(client):
    response = client.delete("/api/v1/data_gathering/delete_all_data")
    assert response.status_code == 202


def test_create_robot(client, delete_all_data):
    response = client.post(
        "/api/v1/data_gathering/robot",
        json={
            "serial_number": "SN000"
        },
    )
    assert response.status_code == 201
    print("this will execute")
    assert response.json() == {'serial_number': 'SN000'}


def test_get_robots(client, delete_all_data):
    response = client.get("/api/v1/data_gathering/robots")
    assert response.status_code == 200
    assert response.json() == []
