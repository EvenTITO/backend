from ..common import create_headers


async def test_get_all_users(client, post_users, admin_data):
    response = await client.get(
        "/users",
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 200
    all_users = response.json()
    ids = post_users
    ids.append(admin_data.id)
    assert len(all_users) == len(ids)
    for user in all_users:
        assert user['id'] in ids
