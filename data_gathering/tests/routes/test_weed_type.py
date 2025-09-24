from app.api.database.db import weed_types
from sqlalchemy import insert
from sqlalchemy.dialects import mysql


def test_create_weed_type(client):
    response = client.post(
        "/api/violette/v2/weed_type",
        json={
            "label": "Daisy"
        },
    )
    assert response.status_code == 201
    print("this will execute")
    assert response.json() == {"id": 1, "label": "Daisy"}


def test_get_list_weeds_types_empty(client):
    response = client.get("/api/violette/v2/weeds_types")
    assert response.status_code == 200
    assert response.json() == []


def test_get_list_weeds_types_with_one(client, cursor_cnx):
    query = str(
        insert(weed_types)
        .values(label="Daisy")
        .compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})
    )
    cursor_cnx[0].execute(query)
    cursor_cnx[1].commit()
    response = client.get("/api/violette/v2/weeds_types")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "label": "Daisy"}]


def test_get_list_weeds_types_with_multiple(client, cursor_cnx):
    for weed_name in ["Daisy", "Plantain"]:
        query = str(
            insert(weed_types)
            .values(label=weed_name)
            .compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})
        )
        cursor_cnx[0].execute(query)
        cursor_cnx[1].commit()
    response = client.get("/api/violette/v2/weeds_types")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "label": "Daisy"}, {
        "id": 2, "label": "Plantain"}]
