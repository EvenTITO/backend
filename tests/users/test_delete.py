from app.users.crud import (
    USER_NOT_FOUND_DETAIL,
)
from ..common import create_headers


def test_delete_user(client, post_user, get_user):
    id_user = post_user()['id']
    response = client.delete(
        f"/users/{id_user}",
        headers=create_headers(id_user)
    )

    assert response.status_code == 204

    get_response = get_user(id_user)
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == USER_NOT_FOUND_DETAIL


def test_delete_user_not_exists(client):
    id_user = "this-id-does-not-exist"
    response = client.delete(
        f"/users/{id_user}",
        headers=create_headers(id_user)
    )

    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND_DETAIL
