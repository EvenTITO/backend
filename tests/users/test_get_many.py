from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from app.schemas.users.user import UserSchema
from ..commontest import create_headers

USERS = [
    UserSchema(
        name="Lucia",
        lastname="Benitez",
        email="lbenitez@email.com",
    ),
    UserSchema(
        name="Marta",
        lastname="Benitez",
        email="mbenitez@email.com",
    ),
    UserSchema(
        name="Pedro",
        lastname="Benitez",
        email="pbenitez@email.com",
    )
]


async def test_get_all_users(client, admin_data):
    ids = []
    for user in USERS:
        id = str(uuid4())
        _ = await client.post(
            "/users",
            json=jsonable_encoder(user),
            headers=create_headers(id)
        )
        ids.append(id)

    response = await client.get(
        "/users",
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 200
    all_users = response.json()

    ids.append(admin_data.id)
    assert len(all_users) == len(ids)
    for user in all_users:
        assert user['id'] in ids
