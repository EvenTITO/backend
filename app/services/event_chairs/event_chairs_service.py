from app.database.models.chair import ChairModel
from app.database.models.user import UserModel
from app.exceptions.members.chair.chair_exceptions import UserNotIsChair
from app.repository.chairs_repository import ChairRepository
from app.repository.users_repository import UsersRepository
from app.schemas.members.chair_schema import ChairResponseSchema, ChairRequestSchema
from app.schemas.users.user import UserSchema
from app.services.events.events_service import EventsService
from app.services.services import BaseService


class EventChairService(BaseService):
    def __init__(
            self,
            event_service: EventsService,
            chair_repository: ChairRepository,
            users_repository: UsersRepository
    ):
        self.event_service = event_service
        self.chair_repository = chair_repository
        self.users_repository = users_repository

    async def get_all_chairs(self, event_id: str):
        users_chairs = await self.chair_repository.get_all(event_id)
        return list(map(EventChairService.__map_to_schema, users_chairs))

    async def get_chair(self, event_id: str, user_id: str):
        if not await self.chair_repository.is_member(event_id, user_id):
            raise UserNotIsChair(event_id, user_id)
        chair = await self.chair_repository.get_member(event_id, user_id)
        return EventChairService.__map_to_schema(chair)

    async def remove_chair(self, event_id: str, user_id: str) -> None:
        if not await self.chair_repository.is_member(event_id, user_id):
            raise UserNotIsChair(event_id, user_id)
        await self.chair_repository.remove_member(event_id, user_id)

    async def is_chair(self, event_id: str, user_id: str) -> None:
        return await self.chair_repository.is_member(event_id, user_id)

    async def update_tracks(self, event_id: str, user_id: str, tracks_schema: ChairRequestSchema) -> None:
        if not await self.chair_repository.is_member(event_id, user_id):
            raise UserNotIsChair(event_id, user_id)
        event_tracks = await self.event_service.get_event_tracks(event_id)
        valid_tracks = []
        for new_track in tracks_schema.tracks:
            if new_track not in event_tracks:
                continue
            valid_tracks.append(new_track)
        await self.chair_repository.update_tracks(event_id, user_id, valid_tracks)

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
