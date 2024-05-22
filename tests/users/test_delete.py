from app.users.crud import (
    USER_NOT_FOUND_DETAIL,
)
from ..common import create_headers


def test_delete_user(client, user_data):
    caller_id = user_data.pop("id")
    response = client.delete(f"/users/{caller_id}",
                             headers=create_headers(caller_id))
    assert response.status_code == 204
    get_response = client.get(f"/users/{caller_id}",
                              headers=create_headers(caller_id))
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == USER_NOT_FOUND_DETAIL


def test_delete_user_not_exists(client, user_data):
    user_data['id'] = "this-id-does-not-exist"
    response = client.delete(f"/users/{user_data['id']}",
                             headers=create_headers(user_data['id']))

    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND_DETAIL
