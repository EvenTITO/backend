from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, TIMESTAMP, func
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class DateTemplate:
    creation_date = Column(DateTime, default=datetime.now(), nullable=False)
    last_update = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())


@declarative_mixin
class ModelTemplate(DateTemplate):
    id = Column(String, default=lambda: str(uuid4()), primary_key=True)
