from app.schemas.members.member_schema import MemberRequestSchema, MemberResponseSchema


class ChairRequestSchema(MemberRequestSchema):
    tracks: list[str]


class ChairResponseSchema(MemberResponseSchema):
    tracks: list[str]
