from app.exceptions.users_exceptions import UserNotFound
from app.organizers.schemas import OrganizerRequestSchema
from app.repository.organizers_repository import OrganizersRepository
from app.repository.users_repository import UsersRepository
from app.services.services import BaseService
from datetime import datetime
from datetime import timedelta

INVITE_ORGANIZER_EXPIRATION_TIME = timedelta(days=20)


class EventOrganizersService(BaseService):
    def __init__(self, organizers_repository: OrganizersRepository, users_repository: UsersRepository, event_id: str):
        self.organizers_repository = organizers_repository
        self.users_repository = users_repository
        self.event_id = event_id

    async def invite(self, organizer: OrganizerRequestSchema):
        organizer_id = await self.users_repository.get_user_id_by_email(organizer.email_organizer)
        if organizer_id is None:
            raise UserNotFound(organizer.email_organizer)
        invite_expiration_date = datetime.now() + INVITE_ORGANIZER_EXPIRATION_TIME
        organizer = await self.organizers_repository.create(
            self.event_id,
            organizer_id,
            expiration_date=invite_expiration_date
        )
        return organizer_id

    async def get_organizers(self):
        organizers = await self.organizers_repository.get_event_organizers(self.event_id)
        return organizers

    async def is_organizer(self, user_id):
        return await self.organizers_repository.is_organizer(self.event_id, user_id)
