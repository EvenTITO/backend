from app.exceptions.users_exceptions import UserNotFound
from app.organizers.schemas import OrganizerRequestSchema
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
        return await self.organizers_repository.is_organizer(event_id, user_id)
