from app.utils.authorization import NOT_PERMISSION_ERROR
from app.users.model import UserPermission
from app.users.schemas import UserSchema, RoleSchema
from fastapi.encoders import jsonable_encoder
from ..common import create_headers, get_user


def test_basic_user_has_no_permission(client, user_data):
    response = client.get(f"/users/{user_data['id']}",
                          headers=create_headers(user_data['id']))
    assert response.status_code == 200
    assert response.json()["role"] == UserPermission.NO_PERMISSION.value


def test_change_permission_to_admin(admin_data, client, user_data):
    new_role = RoleSchema(
        role=UserPermission.ADMIN.value
    )
    response = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204
    user = get_user(client, user_data['id'])

    assert user['id'] == user_data['id']
    assert user['role'] == UserPermission.ADMIN.value


def test_change_permission_to_event_creator(admin_data, client, user_data):
    new_role = RoleSchema(
        role=UserPermission.EVENT_CREATOR.value
    )
    response = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204
    user = get_user(client, user_data['id'])
    assert user['id'] == user_data['id']
    assert user['role'] == UserPermission.EVENT_CREATOR.value


def test_admin_deletes_other_admin_permission(admin_data, client, user_data):
    # changes user_data to ADMIN
    new_role = RoleSchema(
        role=UserPermission.ADMIN.value
    )
    _ = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    # changes user_data to NO_PERMISSION
    new_role = RoleSchema(
        role=UserPermission.NO_PERMISSION.value
    )
    response = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 204

    user = get_user(client, user_data['id'])
    assert user['role'] == UserPermission.NO_PERMISSION.value


def test_admin_deletes_other_event_creator_permission(
    admin_data,
    client,
    user_data
):
    # changes user_data to EVENT_CREATOR
    new_role = RoleSchema(
        role=UserPermission.EVENT_CREATOR.value
    )
    _ = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    # changes user_data to NO_PERMISSION
    new_role = RoleSchema(
        role=UserPermission.NO_PERMISSION.value
    )
    response = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 204
    user = get_user(client, user_data['id'])
    assert user['role'] == UserPermission.NO_PERMISSION.value


def test_not_admin_user_cant_add_admin(client, user_data):
    non_admin_user = UserSchema(
        name="Lio",
        lastname="Messi",
        email="email@email.com"
    )
    non_admin_id = "id-non-admin"
    response = client.post("/users",
                           json=jsonable_encoder(non_admin_user),
                           headers=create_headers(non_admin_id))
    new_role = RoleSchema(
        role=UserPermission.ADMIN.value
    )
    response = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(non_admin_id)
    )
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_PERMISSION_ERROR


def test_not_admin_user_cant_add_creator(client, user_data):
    non_admin_user = UserSchema(
        name="Lio",
        lastname="Messi",
        email="email@email.com"
    )
    non_admin_id = "id-non-admin"
    response = client.post("/users",
                           json=jsonable_encoder(non_admin_user),
                           headers=create_headers(non_admin_id))
    new_role = RoleSchema(
        role=UserPermission.EVENT_CREATOR.value
    )
    response = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(non_admin_id)
    )
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_PERMISSION_ERROR


def test_creator_user_cant_add_other_creator(admin_data, client, user_data):
    creator_role = RoleSchema(
        role=UserPermission.EVENT_CREATOR.value
    )
    client.patch(
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
    client.post(
        "/users",
        json=jsonable_encoder(default_role_user),
        headers=create_headers(default_user_id)
    )

    response = client.patch(
        f"/users/permissions/{default_user_id}",
        json=jsonable_encoder(creator_role),
        headers=create_headers(user_data['id'])
    )
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_PERMISSION_ERROR


def test_user_without_permissions_cant_delete_other_admin(
    admin_data,
    client,
    user_data
):
    # user is trying to change admin_data to NO_PERMISSION
    new_role = RoleSchema(
        role=UserPermission.NO_PERMISSION.value
    )
    response = client.patch(
        f"/users/permissions/{admin_data.id}",
        json=jsonable_encoder(new_role),
        headers=create_headers(user_data['id'])
    )

    assert response.status_code == 403
    assert response.json()['detail'] == NOT_PERMISSION_ERROR


def test_event_creator_cant_delete_other_admin(admin_data, client, user_data):
    # changes user_data to EVENT_CREATOR
    new_role = RoleSchema(
        role=UserPermission.EVENT_CREATOR.value
    )
    _ = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    # user is trying to change admin_data to NO_PERMISSION
    new_role = RoleSchema(
        role=UserPermission.NO_PERMISSION.value
    )
    response = client.patch(
        f"/users/permissions/{admin_data.id}",
        json=jsonable_encoder(new_role),
        headers=create_headers(user_data['id'])
    )

    assert response.status_code == 403
    assert response.json()['detail'] == NOT_PERMISSION_ERROR


def test_admin_can_change_self(client, admin_data, user_data):
    # add another admin
    new_role = RoleSchema(
        role=UserPermission.ADMIN.value
    )
    _ = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    new_role = RoleSchema(
        role=UserPermission.NO_PERMISSION.value
    )
    response = client.patch(
        f"/users/permissions/{admin_data.id}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 204

    user = get_user(client, admin_data.id)
    assert user['role'] == UserPermission.NO_PERMISSION.value
