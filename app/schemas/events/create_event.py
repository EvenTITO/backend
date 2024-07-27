from app.schemas.events.schemas import DynamicEventSchema, StaticEventSchema


class CreateEventSchema(StaticEventSchema, DynamicEventSchema):
    pass
