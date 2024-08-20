from app.database.models.chair import ChairModel
from app.database.models.user import UserModel
from app.exceptions.members.chair.chair_exceptions import AlreadyChairExist, UserNotIsChair
from app.exceptions.users_exceptions import UserNotFound
from app.repository.chairs_repository import ChairRepository
from app.repository.users_repository import UsersRepository
from app.schemas.members.chair_schema import ChairRequestSchema, ChairResponseSchema
from app.schemas.users.user import UserSchema
from app.services.services import BaseService


class EventChairService(BaseService):
    def __init__(self, chair_repository: ChairRepository, users_repository: UsersRepository):
        self.chair_repository = chair_repository
        self.users_repository = users_repository

    async def get_all_chairs(self, event_id: str):
        users_chairs = await self.chair_repository.get_all(event_id)
        return list(map(EventChairService.__map_to_schema, users_chairs))

    async def is_chair(self, event_id: str, user_id: str):
        return await self.chair_repository.is_member(event_id, user_id)

    async def invite_chair(self, chair: ChairRequestSchema, event_id: str):
        user_id = await self.users_repository.get_user_id_by_email(chair.email)
        if user_id is None:
            raise UserNotFound(chair.email)
        if await self.chair_repository.is_member(event_id, user_id):
            raise AlreadyChairExist(event_id, user_id)
        await self.chair_repository.create_member(event_id, user_id)
        return user_id

    async def remove_chair(self, event_id: str, user_id: str) -> None:
        if not await self.chair_repository.is_member(event_id, user_id):
            raise UserNotIsChair(event_id, user_id)
        await self.chair_repository.remove_member(event_id, user_id)

    @staticmethod
    def __map_to_schema(model: (UserModel, ChairModel)) -> ChairResponseSchema:
        user, chair = model
        return ChairResponseSchema(
            event_id=chair.event_id,
            user_id=chair.user_id,
            tracks=chair.tracks,
            user=UserSchema(
                email=user.email,
                name=user.name,
                lastname=user.lastname
            )
        )
