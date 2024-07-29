# flake8: noqa
import pytest
from fastapi.encoders import jsonable_encoder
from app.users.crud import update_permission
from app.users.schemas import RoleSchema
from ..common import create_headers
from uuid import uuid4
from app.users.schemas import UserSchema
from app.users.model import UserPermission
import randomname


@pytest.fixture(scope="function")
def make_user():
    def create_random_user(id_user=None):
        if id_user is None:
            id_user = str(uuid4())
        new_user = UserSchema(
            name=randomname.get_name(),
            lastname=randomname.get_name(),
            email=f"{randomname.get_name()}@gmail.com"
        )

        return {
            'id': id_user,
            'json': jsonable_encoder(new_user)
        }

    return create_random_user


@pytest.fixture(scope="function")
def post_user(make_user, client):
    def make(id_user=None, user_json=None):
        if user_json is None:
            user_dict = make_user(id_user)
            user_json = user_dict['json']
            id_user = user_dict['id']

        _ = client.post(
            f"/users",
            json=user_json,
            headers=create_headers(id_user)
        )

        return {
            'id': id_user,
            'json': user_json
        }

    return make


@pytest.fixture(scope="function")
def post_users(post_user):
    def make(n=1):
        users_dicts = []
        for _ in range(n):
            users_dicts.append(post_user())

        return users_dicts

    return make


@pytest.fixture(scope="function")
def make_admin(post_user, current_session):
    def make(id_user=None, user_json=None):
        if user_json is None:
            user_dict = post_user(id_user=id_user)
            user_json = user_dict['json']
            id_user = user_dict['id']

        user_admin = update_permission(
            current_session,
            id_user,
            UserPermission.ADMIN.value
        )

        return {
            'id': id_user,
            'json': jsonable_encoder(user_admin)
        }

    return make


@pytest.fixture(scope="function")
def make_event_creator(post_user, current_session):
    def make(id_user=None, user_json=None):
        if user_json is None:
            user_dict = post_user(id_user=id_user)
            user_json = user_dict['json']
            id_user = user_dict['id']

        user_admin = update_permission(
            current_session,
            id_user,
            UserPermission.EVENT_CREATOR.value
        )

        return {
            'id': id_user,
            'json': jsonable_encoder(user_admin)
        }

    return make


@pytest.fixture(scope="function")
def get_user(client):
    def get(id_user):
        return client.get(
            f"/users/{id_user}",
            headers=create_headers(id_user)
        )

    return get


@pytest.fixture(scope="function")
def change_role(client):
    def change(super_role_id, user_id, role):
        new_role = RoleSchema(role=role)

        return client.patch(
            f"/users/permissions/{user_id}",
            json=jsonable_encoder(new_role),
            headers=create_headers(super_role_id)
        )

    return change
