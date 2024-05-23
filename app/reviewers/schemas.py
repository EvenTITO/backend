from pydantic import BaseModel


class ReviewerRequestSchema(BaseModel):
    id_reviewer: str


class ReviewerSchema(ReviewerRequestSchema):
    id_event: str
