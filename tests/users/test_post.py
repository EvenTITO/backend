from app.users.schemas import UserSchema
from fastapi.encoders import jsonable_encoder
from ..common import create_headers
# ------------------------------- POST TESTS ------------------------------- #


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


def test_create_same_email_fails(client, user_data):
    new_user_same_email = user_data.copy()
    new_user_same_email.pop("id")
    caller_id = "other-id"
    response = client.post("/users",
                           json=new_user_same_email,
                           headers=create_headers(caller_id))

    print("test_create_same_email_fails:", response.json())

    assert response.status_code == 409
    # assert response.json()["detail"] == EMAIL_ALREADY_EXISTS


def test_create_same_user_twice_fails(client, user_data):
    user_data["email"] = "other-email@email.com"
    caller_id = user_data.pop("id")
    response = client.post("/users",
                           json=user_data,
                           headers=create_headers(caller_id))

    assert response.status_code == 409
    # assert response.json()["detail"] == ID_ALREADY_EXISTS


def test_create_empty_user_fails(client):
    empty_user = {"name": "", "lastname": "", "email": ""}
    response = client.post("/users", json=empty_user,
                           headers=create_headers("a-valid-id"))
    print(response.json())

    assert response.status_code == 422


def test_create_invalid_email_fails(client):
    user_invalid_email = {
        "name": "Juan",
        "lastname": "Perez",
        "email": "invalid_email.com",
    }
    response = client.post("/users", json=user_invalid_email,
                           headers=create_headers("a-valid-id"))

    assert response.status_code == 422
