from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class ModelTemplate:
    id = Column(String, default=lambda: str(uuid4()), primary_key=True)

    creation_date = Column(DateTime, default=datetime.now(), nullable=False)
