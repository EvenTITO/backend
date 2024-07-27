from app.suscriptions.schemas import SuscriptorRequestSchema
import pytest
from fastapi.encoders import jsonable_encoder
from ..common import create_headers


@pytest.fixture(scope="function")
def make_suscription(post_event, post_user):
    def make(id_event=None, id_user=None):
        if id_user is None:
            user_dict = post_user()
            id_user = user_dict['id']

        if id_event is None:
            event_dict = post_event()
            id_event = event_dict['id_event']

        suscription = SuscriptorRequestSchema(
            id_suscriptor=id_user
        )

        return {
            'id_event': id_event,
            'id_suscriptor': id_user,
            'json': jsonable_encoder(suscription)
        }

    return make


@pytest.fixture(scope="function")
def post_suscription(make_suscription, client):
    def post(id_event=None, id_user=None):
        suscription_dict = make_suscription(id_event, id_user)

        id_event = suscription_dict['id_event']
        id_suscriptor = suscription_dict['id_suscriptor']

        _ = client.post(
            f"/events/{id_event}/suscriptions",
            json=suscription_dict['json'],
            headers=create_headers(id_suscriptor)
        )

        return suscription_dict

    return post
