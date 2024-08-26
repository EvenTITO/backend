from pydantic import Field, BaseModel, PrivateAttr

from app.schemas.members.member_schema import MemberResponseSchema


class ReviewerWithWorksResponseSchema(MemberResponseSchema):
    work_ids: list[str] = Field(
        max_length=100,
        examples=[["work_id_01", "work_id_02", "work_id_03"]],
        default_factory=list
    )


class ReviewerResponseSchema(MemberResponseSchema):
    review_deadline: str = Field(examples=["2024-07-12"])
    work_id: str = Field(examples=["work_id_01"])


class ReviewerRequestSchema(BaseModel):
    work_id: str
    email: str
    _user_id: str | None = PrivateAttr()
    review_deadline: str = Field(examples=["2024-07-12"])


class ReviewerCreateRequestSchema(BaseModel):
    reviewers: list[ReviewerRequestSchema] = Field(max_length=50, default_factory=list)
