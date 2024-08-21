from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import declarative_mixin, declared_attr

from app.database.models.utils import DateTemplate


@declarative_mixin
class MemberModel(DateTemplate):

    @declared_attr
    def user_id(self):
        return Column(String, ForeignKey("users.id"), primary_key=True)

    @declared_attr
    def event_id(self):
        return Column(String, ForeignKey("events.id"), primary_key=True)
