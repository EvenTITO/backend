from uuid import uuid4

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class DateTemplate:
    creation_date = Column(DateTime, default=func.now(), nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now())


@declarative_mixin
class ModelTemplate(DateTemplate):
    id = Column(String, default=lambda: str(uuid4()), primary_key=True)
