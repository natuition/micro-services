from app.main import app
from fastapi.testclient import TestClient
import os
import pytest
from databases import DatabaseURL
import mysql.connector as db

DATABASE_URI = os.getenv('DATABASE_URI')
url = DatabaseURL(DATABASE_URI)


@pytest.fixture()
def cursor():
    cnx = db.connect(user=url.username, password=url.password,
                     host=url.hostname, database=url.database)
    cursor = cnx.cursor()
    yield cursor
    cursor.close()
    cnx.close()


@pytest.fixture(autouse=True)
def delete_all_data(cursor):
    cursor.execute("SET foreign_key_checks = 0")
    query = f"SELECT Concat('TRUNCATE TABLE ', TABLE_NAME) FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='{url.database}'"
    cursor.execute(query)
    truncates = cursor.fetchall()
    for truncate in truncates:
        cursor.execute(truncate[0])
    cursor.execute("SET foreign_key_checks = 0")


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_create_robot(client):
    response = client.post(
        "/api/v1/data_gathering/robot",
        json={
            "serial_number": "SN000"
        },
    )
    assert response.status_code == 201
    print("this will execute")
    assert response.json() == {'serial_number': 'SN000'}


def test_get_robots(client):
    response = client.get("/api/v1/data_gathering/robots")
    assert response.status_code == 200
    assert response.json() == []
