from app.main import app
from fastapi.testclient import TestClient
import pytest
import mysql.connector as db
from app.api.database.db import database_url


@pytest.fixture()
def cursor_cnx():
    cnx = db.connect(user=database_url.username, password=database_url.password,
                     host=database_url.hostname, database=database_url.database)
    cursor = cnx.cursor()
    yield cursor, cnx
    cursor.close()
    cnx.close()


@pytest.fixture(autouse=True)
def delete_all_data(cursor_cnx):
    cursor_cnx[0].execute("SET foreign_key_checks = 0")
    query = f"SELECT Concat('TRUNCATE TABLE ', TABLE_NAME) FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='{database_url.database}'"
    cursor_cnx[0].execute(query)
    truncates = cursor_cnx[0].fetchall()
    for truncate in truncates:
        cursor_cnx[0].execute(truncate[0])
    cursor_cnx[0].execute("SET foreign_key_checks = 0")


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client
