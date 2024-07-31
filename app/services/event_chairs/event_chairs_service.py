from datetime import timedelta, datetime

from app.database.models.chair import ChairModel
from app.database.models.member import InvitationStatus
from app.database.models.user import UserModel
from app.exceptions.members.chair.chair_exceptions import NotExistChairInvitation, CannotUpdateChairInvitation
from app.exceptions.users_exceptions import UserNotFound
from app.repository.chairs_repository import ChairRepository
from app.repository.users_repository import UsersRepository
from app.schemas.members.chair_schema import ChairRequestSchema, ChairResponseSchema
from app.schemas.users.user import UserSchema
from app.services.services import BaseService

INVITE_ORGANIZER_EXPIRATION_TIME = timedelta(days=20)


class EventChairService(BaseService):
    def __init__(self, chair_repository: ChairRepository, users_repository: UsersRepository):
        self.chair_repository = chair_repository
        self.users_repository = users_repository

    async def get_all_chairs(self, event_id: str):
        users_chairs = await self.chair_repository.get_all_chairs(event_id)
        return list(map(EventChairService.__map_to_schema, users_chairs))

    async def get_all_chairs_by_status(self, event_id: str, status: InvitationStatus):
        users_chairs = await self.chair_repository.get_all_chairs_by_status(event_id, status)
        return list(map(EventChairService.__map_to_schema, users_chairs))

    async def invite_chair(self, chair: ChairRequestSchema, event_id: str):
        chair_id = await self.users_repository.get_user_id_by_email(chair.email)
        if chair_id is None:
            raise UserNotFound(chair.email)
        invite_expiration_date = datetime.now() + INVITE_ORGANIZER_EXPIRATION_TIME
        if await self.chair_repository.has_invitation_pending(event_id, chair_id):
            return await self.chair_repository.update_expiration_date(event_id, chair_id, invite_expiration_date)
        await self.chair_repository.create_chair(event_id, chair_id, invite_expiration_date, chair.tracks)
        return chair_id

    async def accept_chair_invitation(self, user_id: str, event_id: str):
        conditions = [ChairModel.user_id == user_id, ChairModel.event_id == event_id]
        if not await self.chair_repository.exists(conditions):
            raise NotExistChairInvitation(event_id, user_id)
        chair = await self.chair_repository.get_chair(event_id, user_id)
        if chair.invitation_status != InvitationStatus.INVITED or chair.invitation_expiration_date < datetime.now():
            raise CannotUpdateChairInvitation(event_id, user_id)
        await self.chair_repository.update_invitation(event_id, user_id, status_modification)

    @staticmethod
    def __map_to_schema(model: (UserModel, ChairModel)) -> ChairResponseSchema:
        user, chair = model
        return ChairResponseSchema(
            event_id=chair.event_id,
            user_id=chair.user_id,
            invitation_date=chair.creation_date,
            tracks=chair.tracks,
            user=UserSchema(
                email=user.email,
                name=user.name,
                lastname=user.lastname
            )
        )
