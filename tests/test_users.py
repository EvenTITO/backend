from app.schemas.users import UserSchema
from fastapi.encoders import jsonable_encoder
from app.crud.users import (
    USER_NOT_FOUND_DETAIL,
    EMAIL_ALREADY_EXISTS,
    ID_ALREADY_EXISTS,
)
from .common import create_headers

# ------------------------------- POST TESTS ------------------------------- #


def test_create_user(client):
    user_id = "aasjdfvhasdvnlaksdj"
    user_data = UserSchema(
        name="Lio",
        surname="Messi",
        email="email@email.com"
    )
    response = client.post("/users/",
                           json=jsonable_encoder(user_data),
                           headers=create_headers(user_id))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id"] == user_id
    assert response_data["name"] == user_data.name
    assert response_data["surname"] == user_data.surname
    assert response_data["email"] == user_data.email


def test_create_same_email_fails(client, user_data):
    new_user_same_email = user_data.copy()
    new_user_same_email.pop("id")
    caller_id = "other-id"
    response = client.post("/users/",
                           json=new_user_same_email,
                           headers=create_headers(caller_id))

    print("test_create_same_email_fails:", response.json())

    assert response.status_code == 409
    assert response.json()["detail"] == EMAIL_ALREADY_EXISTS


def test_create_same_user_twice_fails(client, user_data):
    user_data["email"] = "other-email@email.com"
    caller_id = user_data.pop("id")
    response = client.post("/users/",
                           json=user_data,
                           headers=create_headers(caller_id))

    assert response.status_code == 409
    assert response.json()["detail"] == ID_ALREADY_EXISTS


def test_create_empty_user_fails(client):
    empty_user = {"name": "", "surname": "", "email": ""}
    response = client.post("/users/", json=empty_user,
                           headers=create_headers("a-valid-id"))
    print(response.json())

    assert response.status_code == 422


def test_create_invalid_email_fails(client):
    user_invalid_email = {
        "name": "Juan",
        "surname": "Perez",
        "email": "invalid_email.com",
    }
    response = client.post("/users/", json=user_invalid_email,
                           headers=create_headers("a-valid-id"))

    assert response.status_code == 422


# ------------------------------- GET TESTS ------------------------------- #


def test_get_user(client, user_data):
    response = client.get(f"/users/{user_data['id']}",
                          headers=create_headers(user_data['id']))
    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]


def test_get_user_not_exists_fails(client, user_data):
    user_data['id'] = "this-id-does-not-exist"
    response = client.get(f"/users/{user_data['id']}",
                          headers=create_headers(user_data['id']))
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND_DETAIL


# ------------------------------- PUT TESTS ------------------------------- #


def test_put_user(client, user_data):
    update_user_data = user_data.copy()
    update_user_data["name"] = "new name"
    update_user_data["surname"] = "new surname"
    caller_id = update_user_data.pop('id')
    response = client.put("/users/", json=update_user_data,
                          headers=create_headers(caller_id))

    assert response.status_code == 200
    assert response.json()["name"] == update_user_data["name"]
    assert response.json()["surname"] == update_user_data["surname"]


def test_put_user_not_exists(client, user_data):
    user_changes = user_data.copy()
    different_id = "this-id-does-not-exist"
    new_surname = "Rocuzzo"
    user_changes.pop('id')
    user_changes["surname"] = new_surname
    response = client.put("/users/", json=user_changes,
                          headers=create_headers(different_id))
    assert response.status_code == 404


# ------------------------------- DELETE TESTS ------------------------------ #


def test_delete_user(client, user_data):
    caller_id = user_data.pop("id")
    response = client.delete(f"/users/{caller_id}",
                             headers=create_headers(caller_id))
    assert response.status_code == 200
    get_response = client.get(f"/users/{caller_id}",
                              headers=create_headers(caller_id))
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == USER_NOT_FOUND_DETAIL


def test_delete_user_not_exists(client, user_data):
    user_data['id'] = "this-id-does-not-exist"
    response = client.delete(f"/users/{user_data['id']}",
                             headers=create_headers(user_data['id']))

    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND_DETAIL
