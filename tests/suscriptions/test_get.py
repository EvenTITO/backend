from ..common import create_headers


def test_get_suscription(client, post_suscription):
    suscription_dict = post_suscription()
    id_event = suscription_dict['id_event']
    id_suscriptor = suscription_dict['id_suscriptor']

    response = client.get(f"/events/{id_event}/suscriptions")

    assert response.status_code == 200
    suscriptions = response.json()
    assert len(suscriptions) == 1
    assert (suscriptions[0]['id_suscriptor'] ==
            id_suscriptor)


def test_user_suscribes_to_two_events(client, post_suscription):
    suscription_dict1 = post_suscription()
    id_suscriptor = suscription_dict1['id_suscriptor']

    suscription_dict2 = post_suscription(id_user=id_suscriptor)

    response = client.get(
        f"/users/{id_suscriptor}/suscriptions",
        headers=create_headers(id_suscriptor)
    )

    assert response.status_code == 200

    suscriptions_response = response.json()
    assert len(suscriptions_response) == 2
    assert suscriptions_response[0]['id_event'] == suscription_dict1['id_event']
    assert suscriptions_response[1]['id_event'] == suscription_dict2['id_event']
