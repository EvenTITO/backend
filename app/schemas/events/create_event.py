from app.schemas.events.review_skeleton.review_skeleton import ReviewSkeletonRequestSchema
from app.schemas.events.schemas import DynamicEventSchema, StaticEventSchema


class CreateEventSchema(StaticEventSchema, DynamicEventSchema, ReviewSkeletonRequestSchema):
    pass
