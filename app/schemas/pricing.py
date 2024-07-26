from pydantic import (
    BaseModel,
    Field,
)


class FeeSchema(BaseModel):
    name: str = Field(examples=['Students Only Fee']),
    description: str = Field(examples=['Only Students with certificate']),
    value: int = Field(examples=[50]),
    currency: str = Field(examples=['ARS'], default='ARS')
    need_verification: bool = Field(
        description='If it is set to True,'
        ' a validation file must be added in the inscription form'
    )


class PricingSchema(BaseModel):
    rates: list[FeeSchema]
