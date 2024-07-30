from fastapi import HTTPException
from app.database.models.organizer import InvitationStatus
from app.exceptions.expiration_date_exception import ExpirationDateException
from app.exceptions.users_exceptions import UserNotFound
from app.schemas.organizers.schemas import ModifyInvitationStatusSchema, OrganizerRequestSchema
from app.repository.organizers_repository import OrganizersRepository
from app.repository.users_repository import UsersRepository
from app.services.services import BaseService
from datetime import datetime
from datetime import timedelta

INVITE_ORGANIZER_EXPIRATION_TIME = timedelta(days=20)


class EventOrganizersService(BaseService):
    def __init__(self, organizers_repository: OrganizersRepository, users_repository: UsersRepository):
        self.organizers_repository = organizers_repository
        self.users_repository = users_repository

    async def invite(self, organizer: OrganizerRequestSchema, event_id: str):
        organizer_id = await self.users_repository.get_user_id_by_email(organizer.email_organizer)
        if organizer_id is None:
            raise UserNotFound(organizer.email_organizer)
        invite_expiration_date = datetime.now() + INVITE_ORGANIZER_EXPIRATION_TIME
        organizer = await self.organizers_repository.create(
            event_id,
            organizer_id,
            expiration_date=invite_expiration_date
        )
        return organizer_id

    async def get_organizers(self, event_id: str):
        organizers = await self.organizers_repository.get_event_organizers(event_id)
        return organizers

    async def is_organizer(self, event_id: str, user_id: str):
        organizer = await self.organizers_repository.get_organizer(event_id, user_id)
        if organizer is None or organizer.invitation_status != InvitationStatus.ACCEPTED:
            return False
        return True

    async def update_invitation_status(
        self,
        user_id: str,
        event_id: str,
        status_modification: ModifyInvitationStatusSchema
    ):
        if status_modification.invitation_status == InvitationStatus.INVITED:
            raise HTTPException(status_code=400)  # TODO: mejor excepcion.
        organizer = await self.organizers_repository.get_organizer(event_id, user_id)
        if organizer is None:
            raise HTTPException(status_code=404)  # TODO: mejor excepcion.
        if organizer.invitation_status == InvitationStatus.REJECTED:
            raise HTTPException(status_code=409)  # TODO: mejor excepcion.
        if (
            status_modification.invitation_status == InvitationStatus.ACCEPTED and
            organizer.invitation_expiration_date < datetime.now()
        ):
            await self.organizers_repository.delete(event_id, user_id)
            raise ExpirationDateException()

        await self.organizers_repository.update_invitation(event_id, user_id, status_modification)
