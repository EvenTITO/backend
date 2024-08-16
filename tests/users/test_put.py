from ..commontest import create_headers


async def test_put_user(client, create_user):
    update_create_user = create_user.copy()
    update_create_user["name"] = "new name"
    update_create_user["lastname"] = "new lastname"
    caller_id = update_create_user.pop('id')
    response = await client.put("/users/me",
                                json=update_create_user,
                                headers=create_headers(caller_id))

    assert response.status_code == 204
    response = await client.get(f"/users/{caller_id}",
                                headers=create_headers(caller_id))
    assert response.status_code == 200
    assert response.json()["name"] == update_create_user["name"]
    assert response.json()["email"] == update_create_user["email"]
    assert response.json()["lastname"] == update_create_user["lastname"]


async def test_put_user_not_exists(client, create_user):
    user_changes = create_user.copy()
    different_id = "this-id-does-not-exist"
    new_lastname = "Rocuzzo"
    user_changes.pop('id')
    user_changes["lastname"] = new_lastname
    response = await client.put("/users/me",
                                json=user_changes,
                                headers=create_headers(different_id))
    assert response.status_code == 404


async def test_email_cant_change(client, create_user):
    update_create_user = create_user.copy()
    update_create_user["email"] = "nuevo_email@gmail.com"
    caller_id = update_create_user.pop('id')
    response = await client.put("/users/me",
                                json=update_create_user,
                                headers=create_headers(caller_id))

    response = await client.get(f"/users/{caller_id}",
                                headers=create_headers(caller_id))

    assert response.json()["email"] == create_user["email"]
