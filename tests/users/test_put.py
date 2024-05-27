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
