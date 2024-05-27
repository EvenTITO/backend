from app.users.model import UserRole
from app.users.schemas import UserSchema, RoleSchema
from fastapi.encoders import jsonable_encoder
from ..common import create_headers, get_user_method


async def test_basic_user_has_DEFAULT(client, user_data):
    response = await client.get(f"/users/{user_data['id']}",
                                headers=create_headers(user_data['id']))
    assert response.status_code == 200
    assert response.json()["role"] == UserRole.DEFAULT.value


async def test_change_permission_to_admin(admin_data, client, user_data):
    new_role = RoleSchema(
        role=UserRole.ADMIN.value
    )
    response = await client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204
    user = get_user_method(client, user_data['id'])

    assert user['id'] == user_data['id']
    assert user['role'] == UserRole.ADMIN.value


async def test_change_permission_to_event_creator(admin_data, client, user_data):
    new_role = RoleSchema(
        role=UserRole.EVENT_CREATOR.value
    )
    response = await client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204
    user = get_user_method(client, user_data['id'])
    assert user['id'] == user_data['id']
    assert user['role'] == UserRole.EVENT_CREATOR.value


async def test_admin_deletes_other_admin_permission(admin_data, client, user_data):
    # changes user_data to ADMIN
    new_role = RoleSchema(
        role=UserRole.ADMIN.value
    )
    _ = await client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    # changes user_data to DEFAULT
    new_role = RoleSchema(
        role=UserRole.DEFAULT.value
    )
    response = await client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 204

    user = get_user_method(client, user_data['id'])
    assert user['role'] == UserRole.DEFAULT.value


async def test_admin_deletes_other_event_creator_permission(
    admin_data,
    client,
    user_data
):
    # changes user_data to EVENT_CREATOR
    new_role = RoleSchema(
        role=UserRole.EVENT_CREATOR.value
    )
    _ = await client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    # changes user_data to DEFAULT
    new_role = RoleSchema(
        role=UserRole.DEFAULT.value
    )
    response = await client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 204
    user = get_user_method(client, user_data['id'])
    assert user['role'] == UserRole.DEFAULT.value


async def test_not_admin_user_cant_add_admin(client, user_data):
    non_admin_user = UserSchema(
        name="Lio",
        lastname="Messi",
        email="email@email.com"
    )
    non_admin_id = "id-non-admin"
    response = await client.post("/users",
                                 json=jsonable_encoder(non_admin_user),
                                 headers=create_headers(non_admin_id))
    new_role = RoleSchema(
        role=UserRole.ADMIN.value
    )
    response = await client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(non_admin_id)
    )
    assert response.status_code == 403


async def test_not_admin_user_cant_add_creator(client, user_data):
    non_admin_user = UserSchema(
        name="Lio",
        lastname="Messi",
        email="email@email.com"
    )
    non_admin_id = "id-non-admin"
    response = await client.post("/users",
                                 json=jsonable_encoder(non_admin_user),
                                 headers=create_headers(non_admin_id))
    new_role = RoleSchema(
        role=UserRole.EVENT_CREATOR.value
    )
    response = await client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(non_admin_id)
    )
    assert response.status_code == 403


async def test_creator_user_cant_add_other_creator(admin_data, client, user_data):
    creator_role = RoleSchema(
        role=UserRole.EVENT_CREATOR.value
    )
    await client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(creator_role),
        headers=create_headers(admin_data.id)
    )

    default_role_user = UserSchema(
        name="Lio",
        lastname="Messi",
        email="email@email.com"
    )
    default_user_id = "id-default-user"
    await client.post(
        "/users",
        json=jsonable_encoder(default_role_user),
        headers=create_headers(default_user_id)
    )

    response = await client.patch(
        f"/users/permissions/{default_user_id}",
        json=jsonable_encoder(creator_role),
        headers=create_headers(user_data['id'])
    )
    assert response.status_code == 403


async def test_user_without_permissions_cant_delete_other_admin(
    admin_data,
    client,
    user_data
):
    # user is trying to change admin_data to DEFAULT
    new_role = RoleSchema(
        role=UserRole.DEFAULT.value
    )
    response = await client.patch(
        f"/users/permissions/{admin_data.id}",
        json=jsonable_encoder(new_role),
        headers=create_headers(user_data['id'])
    )

    assert response.status_code == 403


async def test_event_creator_cant_delete_other_admin(admin_data, client, user_data):
    # changes user_data to EVENT_CREATOR
    new_role = RoleSchema(
        role=UserRole.EVENT_CREATOR.value
    )
    _ = await client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    # user is trying to change admin_data to DEFAULT
    new_role = RoleSchema(
        role=UserRole.DEFAULT.value
    )
    response = await client.patch(
        f"/users/permissions/{admin_data.id}",
        json=jsonable_encoder(new_role),
        headers=create_headers(user_data['id'])
    )

    assert response.status_code == 403


async def test_admin_can_change_self(client, admin_data, user_data):
    # add another admin
    new_role = RoleSchema(
        role=UserRole.ADMIN.value
    )
    _ = await client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    new_role = RoleSchema(
        role=UserRole.DEFAULT.value
    )
    response = await client.patch(
        f"/users/permissions/{admin_data.id}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 204

    user = get_user_method(client, admin_data.id)
    assert user['role'] == UserRole.DEFAULT.value
