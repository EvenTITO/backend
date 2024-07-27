from app.schemas.events.review_skeleton.review_skeleton import ReviewSkeletonSchema
from app.schemas.events.schemas import DynamicEventSchema, GeneralEventSchema, StaticEventSchema


class EventConfigurationSchema(GeneralEventSchema, DynamicEventSchema, StaticEventSchema):
    review_skeleton: ReviewSkeletonSchema | None
