from ..common import create_headers


def test_put_user(client, user_data):
    update_user_data = user_data.copy()
    update_user_data["name"] = "new name"
    update_user_data["surname"] = "new surname"
    caller_id = update_user_data.pop('id')
    response = client.put(f"/users/{caller_id}",
                          json=update_user_data,
                          headers=create_headers(caller_id))

    assert response.status_code == 204


def test_put_user_not_exists(client, user_data):
    user_changes = user_data.copy()
    different_id = "this-id-does-not-exist"
    new_surname = "Rocuzzo"
    user_changes.pop('id')
    user_changes["surname"] = new_surname
    response = client.put(f"/users/{different_id}",
                          json=user_changes,
                          headers=create_headers(different_id))
    assert response.status_code == 404
