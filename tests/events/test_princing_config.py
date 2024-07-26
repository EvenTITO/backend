from fastapi.encoders import jsonable_encoder
from app.events.schemas import (
    FeeSchema,
    PricingRateSchema
)
from ..common import create_headers


async def test_put_pricing_config(client, admin_data, event_data):
    students_fee = FeeSchema(
        name="Students Only Fee",
        description="Only Students with certificate",
        value="50",
        currency="ARS",
        need_verification=True
    )
    pricing_config = PricingRateSchema(
        rates=[
            students_fee
        ]
    )

    response = await client.put(
        f"/events/{event_data['id']}/configuration/pricing",
        json=jsonable_encoder(pricing_config),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204

    response = await client.get(
        f"/events/{event_data['id']}/pricing",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    print(response.json())
    assert response.json()["rates"][0]["name"] == students_fee.name
