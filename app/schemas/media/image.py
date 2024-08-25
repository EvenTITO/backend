from pydantic import BaseModel, Field


class ImgSchema(BaseModel):
    name: str = Field(max_length=100, examples=["main_image"])
    url: str = Field(max_length=1000, examples=["https://go.com/img.png"])
