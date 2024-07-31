from app.schemas.events.configuration_general import ConfigurationGeneralEventSchema
from app.schemas.events.review_skeleton.review_skeleton import ReviewSkeletonSchema
from app.schemas.events.schemas import DynamicEventSchema, StaticEventSchema


class EventConfigurationSchema(
    ConfigurationGeneralEventSchema,
    DynamicEventSchema,
    StaticEventSchema,
    ReviewSkeletonSchema
):
    pass
