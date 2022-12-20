from app.api.database.db import robots
from sqlalchemy import insert
from sqlalchemy.dialects import mysql


def test_create_robot(client):
    response = client.post(
        "/api/v1/data_gathering/robot",
        json={
            "serial_number": "SN000"
        },
    )
    assert response.status_code == 201
    print("this will execute")
    assert response.json() == {"serial_number": "SN000"}


def test_get_list_robots_empty(client):
    response = client.get("/api/v1/data_gathering/robots")
    assert response.status_code == 200
    assert response.json() == []


def test_get_list_robots_with_one(client, cursor_cnx):
    query = str(
        insert(robots)
        .values(serial_number="SN000")
        .compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})
    )
    cursor_cnx[0].execute(query)
    cursor_cnx[1].commit()
    response = client.get("/api/v1/data_gathering/robots")
    assert response.status_code == 200
    assert response.json() == [{"serial_number": "SN000"}]


def test_get_list_robots_with_multiple(client, cursor_cnx):
    for serial_number in ["SN000", "SN001"]:
        query = str(
            insert(robots)
            .values(serial_number=serial_number)
            .compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})
        )
        cursor_cnx[0].execute(query)
        cursor_cnx[1].commit()
    response = client.get("/api/v1/data_gathering/robots")
    assert response.status_code == 200
    assert response.json() == [{"serial_number": "SN000"}, {
        "serial_number": "SN001"}]
