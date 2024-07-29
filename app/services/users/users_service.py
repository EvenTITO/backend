from app.database.models.user import UserRole
from app.repository import users_crud
from app.repository.users_repository import UsersRepository
from app.schemas.users.user import UserModifySchema, UserReply, UserSchema
from app.services.users.exceptions import (
    EmailAlreadyExists,
    IdAlreadyExists,
    UserNotFound
)
from app.services.services import BaseService


async def get_user_by_id(db, user_id):
    user = await users_crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise UserNotFound(user_id)
    return user


async def get_user_by_email(db, email):
    user = await users_crud.get_user_by_email(db, email)
    if not user:
        raise UserNotFound(email)
    return user


async def get_users(db, skip, limit):
    return await users_crud.get_users(db, skip, limit)


class UsersService(BaseService):
    def __init__(self, users_repository: UsersRepository, user_id: str):
        self.users_repository = users_repository
        self.user_id = user_id

    async def create(self, user: UserSchema) -> str:
        user_in_db = await self.users_repository.get(self.user_id)
        if user_in_db:
            raise IdAlreadyExists(self.user_id)
        user_in_db = await self.users_repository.get_user_by_email(user.email)
        if user_in_db:
            raise EmailAlreadyExists(user.email)

        user_to_create = UserReply(
            **user.model_dump(),
            id=self.user_id,
            role=UserRole.DEFAULT
        )

        user_created = await self.users_repository.create(user_to_create)
        return user_created.id

    async def update(self, user: UserModifySchema):
        await self.users_repository.update(self.user_id, user)

    async def get_role(self):
        return await self.users_repository.get_role(self.user_id)
