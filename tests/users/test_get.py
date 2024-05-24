from ..common import create_headers


def test_get_user(client, user_data):
    response = client.get(f"/users/{user_data['id']}",
                          headers=create_headers(user_data['id']))
    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]


def test_get_no_user_cant_get_other(client, user_data):
    id_new_user = 'user-not-exists'

    response = client.get(f"/users/{user_data['id']}",
                          headers=create_headers(id_new_user))
    assert response.status_code == 404


def test_get_user_not_exists_fails(client, user_data):
    user_data['id'] = "this-id-does-not-exist"
    response = client.get(f"/users/{user_data['id']}",
                          headers=create_headers(user_data['id']))
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == f"User {user_data['id']} not found"


def test_get_all_users(client, post_users, admin_data):
    response = client.get("/users", headers=create_headers(admin_data.id))
    assert response.status_code == 200
    all_users = response.json()
    ids = post_users
    ids.append(admin_data.id)
    assert len(all_users) == len(ids)
    for user in all_users:
        assert user['id'] in ids
