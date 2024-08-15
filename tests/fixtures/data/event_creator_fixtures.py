import pytest
from fastapi.encoders import jsonable_encoder

from app.database.models.user import UserRole
from app.schemas.users.user import UserSchema
from app.schemas.users.user_role import UserRoleSchema
from ...commontest import create_headers, get_user_method


@pytest.fixture(scope="function")
async def event_creator_data(client, admin_data):
    event_creator = UserSchema(
        name="Juan",
        lastname="Martinez",
        email="jmartinez@email.com",
    )
    user_id = await client.post(
        "/users",
        json=jsonable_encoder(event_creator),
        headers=create_headers("lakjsdeuimx213klasmd3")
    )
    user_id = user_id.json()
    new_role = UserRoleSchema(
        role=UserRole.EVENT_CREATOR.value
    )
    _ = await client.patch(
        f"/users/{user_id}/roles",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    event_creator_user = await get_user_method(client, user_id)
    return event_creator_user
