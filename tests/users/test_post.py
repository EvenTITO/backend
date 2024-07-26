from app.schemas.users.user import UserSchema
from fastapi.encoders import jsonable_encoder
from ..common import create_headers
from app.services.users.exceptions import EmailAlreadyExists, IdAlreadyExists


async def test_create_user(client):
    user_id = "aasjdfvhasdvnlaksdj"
    user_data = UserSchema(
        name="Lio",
        lastname="Messi",
        email="email@email.com"
    )
    response = await client.post("/users",
                                 json=jsonable_encoder(user_data),
                                 headers=create_headers(user_id))
    assert response.status_code == 201
    response_data = response.json()
    assert response_data == user_id

    response = await client.get(f"/users/{user_id}",
                                headers=create_headers(user_id))
    assert response.status_code == 200
    assert response.json()["name"] == user_data.name
    assert response.json()["email"] == user_data.email
    assert response.json()["lastname"] == user_data.lastname


async def test_create_same_email_fails(client, user_data):
    new_user_same_email = user_data.copy()
    new_user_same_email.pop("id")
    caller_id = "other-id"
    response = await client.post("/users",
                                 json=new_user_same_email,
                                 headers=create_headers(caller_id))

    expected_error = EmailAlreadyExists(user_data['email'])
    assert response.status_code == 409
    assert response.json()["detail"] == expected_error.detail


async def test_create_same_user_twice_fails(client, user_data):
    user_data["email"] = "other-email@email.com"
    caller_id = user_data.pop("id")
    response = await client.post("/users",
                                 json=user_data,
                                 headers=create_headers(caller_id))

    expected_error = IdAlreadyExists(caller_id)
    assert response.status_code == 409
    assert response.json()["detail"] == expected_error.detail


async def test_create_empty_user_fails(client):
    empty_user = {
        "name": "",
        "lastname": "",
        "email": ""
    }
    response = await client.post("/users", json=empty_user,
                                 headers=create_headers("a-valid-id"))
    print(response.json())

    assert response.status_code == 422


async def test_create_invalid_email_fails(client):
    user_invalid_email = {
        "name": "Juan",
        "lastname": "Perez",
        "email": "invalid_email.com",
    }
    response = await client.post("/users", json=user_invalid_email,
                                 headers=create_headers("a-valid-id"))

    assert response.status_code == 422
