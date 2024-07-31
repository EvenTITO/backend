from datetime import timedelta, datetime

from fastapi import HTTPException

from app.database.models.chair import InvitationStatus, ChairModel
from app.exceptions.chair_exceptions import ChairAlreadyExist, NotExistChairInvitation, CannotUpdateChairInvitation
from app.exceptions.users_exceptions import UserNotFound
from app.repository.chairs_repository import ChairRepository
from app.repository.users_repository import UsersRepository
from app.schemas.members.chair_schema import ChairRequestSchema
from app.schemas.members.member_schema import ModifyInvitationStatusSchema
from app.services.services import BaseService

INVITE_ORGANIZER_EXPIRATION_TIME = timedelta(days=20)


class EventChairService(BaseService):
    def __init__(self, chair_repository: ChairRepository, users_repository: UsersRepository):
        self.chair_repository = chair_repository
        self.users_repository = users_repository

    async def get_chairs(self, event_id: str):
        return await self.chair_repository.get_event_chairs(event_id)

    async def invite_chair(self, chair: ChairRequestSchema, event_id: str):
        chair_id = await self.users_repository.get_user_id_by_email(chair.email)
        if chair_id is None:
            raise UserNotFound(chair.email)
        invite_expiration_date = datetime.now() + INVITE_ORGANIZER_EXPIRATION_TIME
        if self.chair_repository.is_chair(event_id, chair_id):
            raise ChairAlreadyExist(event_id, chair.email)
        await self.chair_repository.create_chair(event_id, chair_id, expiration_date=invite_expiration_date)
        return chair_id

    async def update_chair_invitation_status(
            self,
            user_id: str,
            event_id: str,
            status_modification: ModifyInvitationStatusSchema
    ):
        # TODO: mejorar, esta duplicado con organizer service
        if status_modification.invitation_status == InvitationStatus.INVITED:
            raise HTTPException(status_code=400)
        # TODO usar event_id o id_event unificar
        conditions = [ChairModel.id_chair == user_id, ChairModel.id_event == event_id]
        if not await self.chair_repository.exists(conditions):
            raise NotExistChairInvitation(event_id, user_id)
        chair = await self.chair_repository.get_chair(event_id, user_id)
        if chair.invitation_status != InvitationStatus.INVITED or chair.invitation_expiration_date < datetime.now():
            raise CannotUpdateChairInvitation(event_id, user_id)
        await self.chair_repository.update_invitation(event_id, user_id, status_modification)
