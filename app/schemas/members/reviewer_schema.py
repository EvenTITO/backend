from uuid import UUID

from pydantic import Field, BaseModel, PrivateAttr

from app.schemas.members.member_schema import MemberResponseSchema
from app.schemas.users.utils import UID


class ReviewerWithWorksResponseSchema(MemberResponseSchema):
    work_ids: list[str] = Field(
        max_length=100,
        examples=[["work_id_01", "work_id_02", "work_id_03"]],
        default_factory=list
    )


class ReviewerResponseSchema(MemberResponseSchema):
    review_deadline: str = Field(examples=["2024-07-12"])
    work_id: UUID = Field(examples=["work_id_01"])


class ReviewerRequestSchema(BaseModel):
    work_id: UUID
    email: str
    _user_id: UID | None = PrivateAttr()
    review_deadline: str = Field(examples=["2024-07-12"])


class ReviewerCreateRequestSchema(BaseModel):
    reviewers: list[ReviewerRequestSchema] = Field(max_length=50, default_factory=list)
