from fastapi.encoders import jsonable_encoder
from app.schemas.users.user import UserSchema
from ..common import create_headers
from app.exceptions.users_exceptions import UserNotFound


async def test_get_user(client, user_data):
    response = await client.get(f"/users/{user_data['id']}",
                                headers=create_headers(user_data['id']))
    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]


async def test_get_no_user_cant_get_other(client, user_data):
    id_new_user = 'user-not-exists'

    response = await client.get(f"/users/{user_data['id']}",
                                headers=create_headers(id_new_user))
    expected_error = UserNotFound(id_new_user)
    assert response.status_code == 404
    assert response.json()['detail'] == expected_error.detail


async def test_get_user_from_other_user_forbidden(client, user_data):
    other_user_id = "paoksncaokasdasdl"
    other_user_data = UserSchema(
        name="Lio",
        lastname="Messi",
        email="email@email.com"
    )
    await client.post(
        "/users",
        json=jsonable_encoder(other_user_data),
        headers=create_headers(other_user_id)
    )

    response = await client.get(f"/users/{other_user_id}",
                                headers=create_headers(user_data['id']))
    assert response.status_code == 403


async def test_get_user_from_admin_user_success(client, user_data, admin_data):

    response = await client.get(f"/users/{user_data['id']}",
                                headers=create_headers(admin_data.id))
    assert response.status_code == 200
