import pytest
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from app.schemas.users.user import UserSchema
from ...commontest import create_headers, get_user_method, USERS


@pytest.fixture(scope="function")
async def user_data(client):
    new_user = UserSchema(
        name="Lio",
        lastname="Messi",
        email="lio_messi@email.com",
    )
    response = await client.post(
        "/users",
        json=jsonable_encoder(new_user),
        headers=create_headers("iuaealdasldanfasdlasd")
    )
    user_data_id = response.json()
    user = await get_user_method(client, user_data_id)
    return user


@pytest.fixture(scope="function")
async def post_users(client):
    ids = []
    for user in USERS:
        id = str(uuid4())
        _ = await client.post(
            "/users",
            json=jsonable_encoder(user),
            headers=create_headers(id)
        )
        ids.append(id)
    return ids
