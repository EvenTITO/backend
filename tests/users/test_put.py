from fastapi.encoders import jsonable_encoder
from app.users.schemas import UserSchema
from ..common import create_headers


async def test_put_user(client, user_data):
    update_user_data = user_data.copy()
    update_user_data["name"] = "new name"
    update_user_data["lastname"] = "new lastname"
    caller_id = update_user_data.pop('id')
    response = await client.put(f"/users/{caller_id}",
                                json=update_user_data,
                                headers=create_headers(caller_id))

    assert response.status_code == 204
    response = await client.get(f"/users/{caller_id}",
                                headers=create_headers(caller_id))
    assert response.status_code == 200
    assert response.json()["name"] == update_user_data["name"]
    assert response.json()["email"] == update_user_data["email"]
    assert response.json()["lastname"] == update_user_data["lastname"]


async def test_put_user_not_exists(client, user_data):
    user_changes = user_data.copy()
    different_id = "this-id-does-not-exist"
    new_lastname = "Rocuzzo"
    user_changes.pop('id')
    user_changes["lastname"] = new_lastname
    response = await client.put(f"/users/{different_id}",
                                json=user_changes,
                                headers=create_headers(different_id))
    assert response.status_code == 404


async def test_email_cant_change(client, user_data):
    update_user_data = user_data.copy()
    update_user_data["email"] = "nuevo_email@gmail.com"
    caller_id = update_user_data.pop('id')
    response = await client.put(f"/users/{caller_id}",
                                json=update_user_data,
                                headers=create_headers(caller_id))

    assert response.status_code == 409


async def test_update_user_from_other_user_fails_no_permission(
        client,
        user_data
):
    other_user = UserSchema(
        name="Lio",
        lastname="Messi",
        email="email@email.com"
    )
    other_user_id = 'other-user-id'
    await client.post(
        "/users",
        json=jsonable_encoder(other_user),
        headers=create_headers(other_user_id)
    )

    update_user_data = user_data.copy()
    update_user_data["lastname"] = "New Lastname"
    caller_id = update_user_data.pop('id')
    response = await client.put(
        f"/users/{caller_id}",
        json=update_user_data,
        headers=create_headers(other_user_id)
    )

    assert response.status_code == 403


async def test_update_user_from_admin_user_fails_no_permission(
        client,
        user_data,
        admin_data
):
    update_user_data = user_data.copy()
    update_user_data["lastname"] = "New Lastname"
    caller_id = update_user_data.pop('id')
    response = await client.put(
        f"/users/{caller_id}",
        json=update_user_data,
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 403
