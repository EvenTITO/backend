from ..common import client
from app.schemas.users import UserSchema
from fastapi.encoders import jsonable_encoder
from app.crud.users import USER_NOT_FOUND_DETAIL, \
                EMAIL_ALREADY_EXISTS, ID_ALREADY_EXISTS


first_user_data = UserSchema(
  id="aasjdfvhasdvnlaksdj",
  name="Lio",
  surname="Messi",
  email="email@email.com"
)


# ------------------------------- POST TESTS ------------------------------- #

def test_create_user():
    response = client.post("/users/", json=jsonable_encoder(first_user_data))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data['id'] == first_user_data.id
    assert response_data['name'] == first_user_data.name
    assert response_data['surname'] == first_user_data.surname
    assert response_data['email'] == first_user_data.email


def test_create_same_email_fails():
    new_user_same_email = first_user_data.model_copy()
    new_user_same_email.id = "other-id"
    response = client.post("/users/",
                           json=jsonable_encoder(new_user_same_email))
    print('test_create_same_email_fails:', response.json())

    assert response.status_code == 409
    assert response.json()['detail'] == EMAIL_ALREADY_EXISTS


def test_create_again_fails():
    new_user_same_id = first_user_data.model_copy()
    new_user_same_id.email = "other_email@email.com"
    response = client.post("/users/", json=jsonable_encoder(new_user_same_id))
    print('test_create_again_fails:', response.json())

    assert response.status_code == 409
    assert response.json()['detail'] == ID_ALREADY_EXISTS


def test_create_empty_user_fails():
    empty_user = {
        "id": "1234",
        "name": "",
        "surname": "",
        "email": ""
    }
    response = client.post("/users/", json=empty_user)
    print(response.json())

    assert response.status_code == 422


def test_create_invalid_email_fails():
    user_invalid_email = {
        "id": "1234",
        "name": "Juan",
        "surname": "Perez",
        "email": "invalid_email.com"
    }
    response = client.post("/users/", json=user_invalid_email)

    assert response.status_code == 422


# ------------------------------- GET TESTS ------------------------------- #

def test_get_user():
    response = client.get(f"/users/{first_user_data.id}")
    assert response.status_code == 200
    assert response.json()['name'] == first_user_data.name


def test_get_user_not_exists_fails():
    id = "this-id-does-not-exist"
    response = client.get(f"/users/{id}")
    print(response.json())
    assert response.status_code == 404
    assert response.json()['detail'] == USER_NOT_FOUND_DETAIL


# ------------------------------- PUT TESTS ------------------------------- #

def test_put_user():
    user_changes = first_user_data.model_copy()
    new_name = "Andres"
    new_surname = "Cuccittini"
    user_changes.name = new_name
    user_changes.surname = new_surname
    response = client.put("/users/", json=jsonable_encoder(user_changes))
    print(response.json())
    assert response.status_code == 200
    assert response.json()['name'] == new_name
    assert response.json()['surname'] == new_surname


def test_put_user_not_exists():
    user_changes = first_user_data.model_copy()
    different_id = "this-id-does-not-exist"
    new_surname = "Rocuzzo"
    user_changes.id = different_id
    user_changes.surname = new_surname
    response = client.put("/users/", json=jsonable_encoder(user_changes))
    assert response.status_code == 404

# ------------------------------- DELETE TESTS ------------------------------ #
