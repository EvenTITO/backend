from app.utils.authorization import NOT_PERMISSION_ERROR
from app.users.model import UserPermission
from app.users.schemas import UserSchema, RoleSchema
from fastapi.encoders import jsonable_encoder
from app.users.crud import (
    USER_NOT_FOUND_DETAIL,
    EMAIL_ALREADY_EXISTS,
    ID_ALREADY_EXISTS,
)
from .common import create_headers

# ------------------------------- POST TESTS ------------------------------- #


def test_create_user(client):
    user_id = "aasjdfvhasdvnlaksdj"
    user_data = UserSchema(
        name="Lio",
        surname="Messi",
        email="email@email.com"
    )
    response = client.post("/users/",
                           json=jsonable_encoder(user_data),
                           headers=create_headers(user_id))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id"] == user_id
    assert response_data["name"] == user_data.name
    assert response_data["surname"] == user_data.surname
    assert response_data["email"] == user_data.email


def test_create_same_email_fails(client, user_data):
    new_user_same_email = user_data.copy()
    new_user_same_email.pop("id")
    caller_id = "other-id"
    response = client.post("/users/",
                           json=new_user_same_email,
                           headers=create_headers(caller_id))

    print("test_create_same_email_fails:", response.json())

    assert response.status_code == 409
    assert response.json()["detail"] == EMAIL_ALREADY_EXISTS


def test_create_same_user_twice_fails(client, user_data):
    user_data["email"] = "other-email@email.com"
    caller_id = user_data.pop("id")
    response = client.post("/users/",
                           json=user_data,
                           headers=create_headers(caller_id))

    assert response.status_code == 409
    assert response.json()["detail"] == ID_ALREADY_EXISTS


def test_create_empty_user_fails(client):
    empty_user = {"name": "", "surname": "", "email": ""}
    response = client.post("/users/", json=empty_user,
                           headers=create_headers("a-valid-id"))
    print(response.json())

    assert response.status_code == 422


def test_create_invalid_email_fails(client):
    user_invalid_email = {
        "name": "Juan",
        "surname": "Perez",
        "email": "invalid_email.com",
    }
    response = client.post("/users/", json=user_invalid_email,
                           headers=create_headers("a-valid-id"))

    assert response.status_code == 422


# ------------------------------- GET TESTS ------------------------------- #


def test_get_user(client, user_data):
    response = client.get(f"/users/{user_data['id']}",
                          headers=create_headers(user_data['id']))
    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]


def test_get_user_not_exists_fails(client, user_data):
    user_data['id'] = "this-id-does-not-exist"
    response = client.get(f"/users/{user_data['id']}",
                          headers=create_headers(user_data['id']))
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == USER_NOT_FOUND_DETAIL


# ------------------------------- PUT TESTS ------------------------------- #


def test_put_user(client, user_data):
    update_user_data = user_data.copy()
    update_user_data["name"] = "new name"
    update_user_data["surname"] = "new surname"
    caller_id = update_user_data.pop('id')
    response = client.put("/users/", json=update_user_data,
                          headers=create_headers(caller_id))

    assert response.status_code == 200
    assert response.json()["name"] == update_user_data["name"]
    assert response.json()["surname"] == update_user_data["surname"]


def test_put_user_not_exists(client, user_data):
    user_changes = user_data.copy()
    different_id = "this-id-does-not-exist"
    new_surname = "Rocuzzo"
    user_changes.pop('id')
    user_changes["surname"] = new_surname
    response = client.put("/users/", json=user_changes,
                          headers=create_headers(different_id))
    assert response.status_code == 404


# ------------------------------- DELETE TESTS ------------------------------ #


def test_delete_user(client, user_data):
    caller_id = user_data.pop("id")
    response = client.delete(f"/users/{caller_id}",
                             headers=create_headers(caller_id))
    assert response.status_code == 200
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


# ------------------------------- PERMISSIONS ------------------------------ #

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
    assert response.status_code == 200
    assert response.json()['id'] == user_data['id']
    assert response.json()['role'] == UserPermission.ADMIN.value


def test_change_permission_to_event_creator(admin_data, client, user_data):
    new_role = RoleSchema(
        role=UserPermission.EVENT_CREATOR.value
    )
    response = client.patch(
        f"/users/permissions/{user_data['id']}",
        json=jsonable_encoder(new_role),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 200
    assert response.json()['id'] == user_data['id']
    assert response.json()['role'] == UserPermission.EVENT_CREATOR.value


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

    assert response.status_code == 200
    assert response.json()['role'] == UserPermission.NO_PERMISSION.value


def test_admin_deletes_other_event_creator_permission(admin_data, client, user_data):
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

    assert response.status_code == 200
    assert response.json()['role'] == UserPermission.NO_PERMISSION.value


def test_not_admin_user_cant_add_admin(client, user_data):
    non_admin_user = UserSchema(
        name="Lio",
        surname="Messi",
        email="email@email.com"
    )
    non_admin_id = "id-non-admin"
    response = client.post("/users/",
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
        surname="Messi",
        email="email@email.com"
    )
    non_admin_id = "id-non-admin"
    response = client.post("/users/",
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
        surname="Messi",
        email="email@email.com"
    )
    default_user_id = "id-default-user"
    client.post(
        "/users/",
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


def test_user_without_permissions_cant_delete_other_admin(admin_data, client, user_data):
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

    assert response.status_code == 200
    assert response.json()['role'] == UserPermission.NO_PERMISSION.value
