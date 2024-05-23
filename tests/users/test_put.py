from ..common import create_headers


def test_put_user(client, post_user):
    user_dict = post_user()
    user_json = user_dict['json']
    id_user = user_dict['id']

    user_json['name'] = "new name"
    user_json['lastname'] = "new lastname"

    response = client.put(
        f"/users/{id_user}",
        json=user_json,
        headers=create_headers(id_user)
    )

    assert response.status_code == 204


def test_put_user_not_exists(client, post_user):
    user_dict = post_user()
    user_json = user_dict['json']

    different_id = "this-id-does-not-exist"
    user_json['lastname'] = 'Perecito'
    response = client.put(
        f"/users/{different_id}",
        json=user_json,
        headers=create_headers(different_id))

    assert response.status_code == 404
