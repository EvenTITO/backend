from uuid import uuid4

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.dialects.postgresql import UUID


@declarative_mixin
class DateTemplate:
    creation_date = Column(DateTime, server_default=func.now(), nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now())
# func.now() documentation: https://docs.sqlalchemy.org/en/14/core/defaults.html#client-invoked-sql-expressions


@declarative_mixin
class ModelTemplate(DateTemplate):
    id = Column(UUID(as_uuid=False), primary_key=True, default=uuid4)


# We store UID generated by the auth provider, not UUID.
UIDType = String(128)
