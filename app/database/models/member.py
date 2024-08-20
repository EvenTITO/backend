from sqlalchemy import Column, String, ForeignKey

from app.database.models.utils import DateTemplate


class MemberModel(DateTemplate):
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), primary_key=True)
