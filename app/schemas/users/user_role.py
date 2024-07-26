from app.models.user import UserRole
from pydantic import BaseModel


class UserRoleSchema(BaseModel):
    role: UserRole
