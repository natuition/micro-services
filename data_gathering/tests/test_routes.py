from app.main import app
from app.api.database.db import metadata, DATABASE_URI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
import pytest
from databases import DatabaseURL


@pytest.fixture(autouse=True, scope="session")
def setup_test_database():
    mysql_url = DATABASE_URI.rsplit('/', 1)[0]
    engine = create_engine(mysql_url)  # connect to mysql
    assert not database_exists(
        mysql_url), 'Test database already exists. Aborting tests.'
    test_database_url = str(DatabaseURL(DATABASE_URI).replace(
        database='test_' + DatabaseURL(DATABASE_URI).database))
    create_database(test_database_url)             # Create the test database.
    engine = create_engine(test_database_url)      # Connect to test database.
    metadata.create_all(engine)      # Create the tables.
    yield                            # Run the tests.
    drop_database(test_database_url)               # Drop the test database.


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_get_robots(client):
    response = client.get("/api/v1/data_gathering/robots")
    assert response.status_code == 200
    assert response.json() == []


"""
def test_create_robot(client):
    response = client.post(
        "/api/v1/data_gathering/robot",
        json={
            "serial_number": "SN000"
        },
    )
    assert response.status_code == 201
    assert {
        "serial_number": "SN000",
    } in response.json()"""
