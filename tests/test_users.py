from app.schemas.users import UserSchema
from fastapi.encoders import jsonable_encoder
from app.crud.users import (
    USER_NOT_FOUND_DETAIL,
    EMAIL_ALREADY_EXISTS,
    ID_ALREADY_EXISTS,
)


# ------------------------------- POST TESTS ------------------------------- #


def test_create_user(client):
    user_data = UserSchema(
        id="aasjdfvhasdvnlaksdj",
        name="Lio",
        surname="Messi",
        email="email@email.com"
    )
    response = client.post("/users/", json=jsonable_encoder(user_data))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id"] == user_data.id
    assert response_data["name"] == user_data.name
    assert response_data["surname"] == user_data.surname
    assert response_data["email"] == user_data.email


def test_create_same_email_fails(client, user_data):
    new_user_same_email = user_data.copy()
    new_user_same_email["id"] = "other-id"
    response = client.post("/users/", json=new_user_same_email)

    print("test_create_same_email_fails:", response.json())

    assert response.status_code == 409
    assert response.json()["detail"] == EMAIL_ALREADY_EXISTS


def test_create_same_user_twice_fails(client, user_data):
    user_data["email"] = "other-email@email.com"
    response = client.post("/users/", json=user_data)

    assert response.status_code == 409
    assert response.json()["detail"] == ID_ALREADY_EXISTS


def test_create_empty_user_fails(client):
    empty_user = {"id": "1234", "name": "", "surname": "", "email": ""}
    response = client.post("/users/", json=empty_user)
    print(response.json())

    assert response.status_code == 422


def test_create_invalid_email_fails(client):
    user_invalid_email = {
        "id": "1234",
        "name": "Juan",
        "surname": "Perez",
        "email": "invalid_email.com",
    }
    response = client.post("/users/", json=user_invalid_email)

    assert response.status_code == 422


# ------------------------------- GET TESTS ------------------------------- #


def test_get_user(client, user_data):
    response = client.get(f"/users/{user_data['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]


def test_get_user_not_exists_fails(client):
    id = "this-id-does-not-exist"
    response = client.get(f"/users/{id}")
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND_DETAIL


# ------------------------------- PUT TESTS ------------------------------- #


def test_put_user(client, user_data):
    update_user_data = user_data.copy()
    update_user_data["name"] = "new name"
    update_user_data["surname"] = "new surname"

    response = client.put("/users/", json=update_user_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["name"] == update_user_data["name"]
    assert response.json()["surname"] == update_user_data["surname"]


def test_put_user_not_exists(client, user_data):
    user_changes = user_data.copy()
    different_id = "this-id-does-not-exist"
    new_surname = "Rocuzzo"
    user_changes["id"] = different_id
    user_changes["surname"] = new_surname
    response = client.put("/users/", json=user_changes)
    assert response.status_code == 404


# ------------------------------- DELETE TESTS ------------------------------ #


def test_delete_user(client, user_data):
    id = user_data["id"]
    response = client.delete(f"/users/{id}")
    assert response.status_code == 200
    get_response = client.get(f"/users/{id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == USER_NOT_FOUND_DETAIL


def test_delete_user_not_exists(client):
    id = "this-id-does-not-exist"
    response = client.delete(f"/users/{id}")

    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND_DETAIL
