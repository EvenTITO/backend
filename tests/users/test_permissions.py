from app.utils.authorization import NOT_PERMISSION_ERROR
from app.users.model import UserPermission


def test_basic_user_has_no_permission(post_user, get_user):
    user_dict = post_user()

    response = get_user(user_dict['id'])
    assert response.status_code == 200
    assert response.json()["role"] == UserPermission.NO_PERMISSION.value


def test_change_permission_to_admin(
    post_user,
    make_admin,
    get_user,
    change_role
):
    admin_dict = make_admin()
    common_user_dict = post_user()

    new_role = UserPermission.ADMIN.value
    response = change_role(
        admin_dict['id'],
        common_user_dict['id'],
        new_role
    )
    assert response.status_code == 204
    response_user = get_user(common_user_dict['id'])

    assert response_user.json()['role'] == new_role


def test_change_permission_to_event_creator(
    post_user,
    make_admin,
    get_user,
    change_role
):
    admin_dict = make_admin()
    common_user_dict = post_user()
    new_role = UserPermission.EVENT_CREATOR.value

    response = change_role(
        admin_dict['id'],
        common_user_dict['id'],
        new_role
    )
    assert response.status_code == 204

    response_user = get_user(common_user_dict['id'])
    assert response_user.json()['role'] == new_role


def test_admin_deletes_other_admin_permission(
    make_admin,
    change_role,
    get_user
):
    admin_dict1 = make_admin()
    admin_dict2 = make_admin()
    new_role = UserPermission.NO_PERMISSION.value

    response = change_role(
        admin_dict1['id'],
        admin_dict2['id'],
        new_role
    )
    assert response.status_code == 204

    response_user = get_user(admin_dict2['id'])
    assert response_user.json()['role'] == new_role


def test_admin_deletes_other_event_creator_permission(
    make_admin,
    make_event_creator,
    change_role,
    get_user
):
    admin_dict = make_admin()
    creator_dict = make_event_creator()
    new_role = UserPermission.NO_PERMISSION.value

    response = change_role(
        admin_dict['id'],
        creator_dict['id'],
        new_role
    )
    assert response.status_code == 204

    response_user = get_user(creator_dict['id'])
    assert response_user.json()['role'] == new_role


def test_not_admin_user_cant_add_admin(
    post_user,
    make_admin,
    change_role
):
    admin_dict = make_admin()
    user_dict = post_user()
    new_role = UserPermission.NO_PERMISSION.value

    response = change_role(
        user_dict['id'],
        admin_dict['id'],
        new_role
    )
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_PERMISSION_ERROR


def test_not_admin_user_cant_add_creator(
    post_user,
    change_role
):
    user_dict1 = post_user()
    user_dict2 = post_user()
    new_role = UserPermission.EVENT_CREATOR.value

    response = change_role(
        user_dict1['id'],
        user_dict2['id'],
        new_role
    )
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_PERMISSION_ERROR


def test_creator_user_cant_add_other_creator(
    make_event_creator,
    post_user,
    change_role
):
    creator_dict = make_event_creator()
    user_dict = post_user()
    new_role = UserPermission.EVENT_CREATOR.value

    response = change_role(
        creator_dict['id'],
        user_dict['id'],
        new_role
    )
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_PERMISSION_ERROR


def test_user_without_permissions_cant_delete_other_admin(
    make_admin,
    post_user,
    change_role
):
    admin_dict = make_admin()
    user_dict = post_user()
    new_role = UserPermission.NO_PERMISSION.value

    response = change_role(
        user_dict['id'],
        admin_dict['id'],
        new_role
    )

    assert response.status_code == 403
    assert response.json()['detail'] == NOT_PERMISSION_ERROR


def test_event_creator_cant_delete_other_admin(
    make_admin,
    make_event_creator,
    change_role
):
    admin_dict = make_admin()
    creator_dict = make_event_creator()
    new_role = UserPermission.NO_PERMISSION.value

    response = change_role(
        creator_dict['id'],
        admin_dict['id'],
        new_role
    )

    assert response.status_code == 403
    assert response.json()['detail'] == NOT_PERMISSION_ERROR


def test_admin_can_change_self_if_exists_another(
    make_admin,
    change_role,
    get_user
):
    admin_dict1 = make_admin()
    _ = make_admin()
    new_role = UserPermission.NO_PERMISSION.value

    response = change_role(
        admin_dict1['id'],
        admin_dict1['id'],
        new_role
    )
    assert response.status_code == 204

    response_user = get_user(admin_dict1['id'])
    assert response_user.json()['role'] == new_role


def test_admin_cant_change_self_if_not_exists_another(
    make_admin,
    change_role
):
    admin_dict = make_admin()
    new_role = UserPermission.NO_PERMISSION.value

    response = change_role(
        admin_dict['id'],
        admin_dict['id'],
        new_role
    )
    assert response.status_code == 409
