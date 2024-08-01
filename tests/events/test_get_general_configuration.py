from ..commontest import create_headers


async def test_get_event_configuration_organizer_gets_dates_pricing_review_skeleton_and_emails(
    client,
    user_data,
    event_creator_data,
    event_from_event_creator
):
    response = await client.get(
        f"/events/{event_from_event_creator}/configuration",
        headers=create_headers(event_creator_data["id"])
    )
    event_config = response.json()

    assert response.status_code == 200
    print(response.json())
    assert event_config['dates'] is not None
    assert len(event_config['pricing']) == 0
    assert len(event_config['notification_mails']) == 0
    assert len(event_config['review_skeleton']['questions']) == 0
