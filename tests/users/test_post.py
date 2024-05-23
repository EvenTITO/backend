from app.users.crud import (
    EMAIL_ALREADY_EXISTS,
    ID_ALREADY_EXISTS,
)
from ..common import create_headers


def test_create_user(client, make_user):
    user_dict = make_user()
    response = client.post(
        "/users",
        json=user_dict['json'],
        headers=create_headers(user_dict['id'])
    )
    assert response.status_code == 201

    response_data = response.json()
    assert response_data == user_dict['id']


def test_create_same_email_fails(client, post_user):
    user_dict = post_user()

    caller_id = "other-id"
    response = client.post(
        "/users",
        json=user_dict['json'],
        headers=create_headers(caller_id)
    )

    assert response.status_code == 409
    assert response.json()["detail"] == EMAIL_ALREADY_EXISTS


def test_create_same_user_twice_fails(client, post_user):
    user_dict = post_user()
    user_json = user_dict['json']
    id_user = user_dict['id']

    user_json['email'] = "other-email@email.com"

    response = client.post(
        "/users",
        json=user_json,
        headers=create_headers(id_user)
    )

    assert response.status_code == 409
    assert response.json()["detail"] == ID_ALREADY_EXISTS


def test_create_empty_user_fails(client):
    empty_user = {"name": "", "lastname": "", "email": ""}
    response = client.post(
        "/users",
        json=empty_user,
        headers=create_headers("a-valid-id")
    )

    assert response.status_code == 422


def test_create_invalid_email_fails(client):
    user_invalid_email = {
        "name": "Juan",
        "lastname": "Perez",
        "email": "invalid_email.com",
    }
    response = client.post(
        "/users",
        json=user_invalid_email,
        headers=create_headers("a-valid-id")
    )

    assert response.status_code == 422
