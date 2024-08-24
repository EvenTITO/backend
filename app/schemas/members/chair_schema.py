from app.schemas.events.schemas import DynamicTracksEventSchema
from app.schemas.members.member_schema import MemberResponseSchema


class ChairResponseSchema(MemberResponseSchema, DynamicTracksEventSchema):
    pass
