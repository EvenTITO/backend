from fastapi.encoders import jsonable_encoder
from app.schemas.events.pricing import (
    FeeSchema,
    PricingSchema
)
from ..commontest import create_headers


async def test_put_pricing_config(client, admin_data, create_event):
    students_fee = FeeSchema(
        name="Students Only Fee",
        description="Only Students with certificate",
        value="50",
        currency="ARS",
        need_verification=True
    )
    pricing_config = PricingSchema(
        pricing=[
            students_fee
        ]
    )

    response = await client.put(
        f"/events/{create_event['id']}/configuration/pricing",
        json=jsonable_encoder(pricing_config),
        headers=create_headers(admin_data.id)
    )
    assert response.status_code == 204

    response = await client.get(
        f"/events/{create_event['id']}/public",
        headers=create_headers(admin_data.id)
    )

    assert response.status_code == 200
    assert response.json()["pricing"][0]["name"] == students_fee.name
