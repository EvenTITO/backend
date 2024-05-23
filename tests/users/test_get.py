from app.users.crud import (
    USER_NOT_FOUND_DETAIL,

)
from ..common import create_headers


def test_get_user(client, post_user):
    user_dict = post_user()

    response = client.get(
        f"/users/{user_dict['id']}",
        headers=create_headers(user_dict['id'])
    )
    assert response.status_code == 200
    assert response.json()["name"] == user_dict["json"]['name']


def test_get_user_not_exists_fails(client):
    id_fake_user = "this-id-does-not-exist"
    response = client.get(
        f"/users/{id_fake_user}",
        headers=create_headers(id_fake_user)
    )

    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND_DETAIL


def test_get_all_users(client, make_admin, post_users):
    admin_dict = make_admin()
    N_USERS = 3
    users_dicts = post_users(n=N_USERS)

    response = client.get(
        "/users",
        headers=create_headers(admin_dict['id'])
    )
    assert response.status_code == 200

    all_users = response.json()
    ids_users = [user['id'] for user in all_users]
    assert len(all_users) == N_USERS + 1
    for user in users_dicts:
        assert user['id'] in ids_users

    assert admin_dict['id'] in ids_users
