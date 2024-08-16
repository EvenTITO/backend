import pytest
from fastapi.encoders import jsonable_encoder
from app.schemas.users.user import UserSchema

from ...commontest import create_headers, get_user_method


@pytest.fixture(scope="function")
async def create_user(client):
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
    create_user_id = response.json()
    user = await get_user_method(client, create_user_id)
    return user