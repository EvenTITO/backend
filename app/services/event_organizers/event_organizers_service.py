from datetime import datetime
from datetime import timedelta

from app.database.models.member import InvitationStatus, MemberModel
from app.database.models.user import UserModel
from app.exceptions.members.organizer.organizer_exceptions import ExpiredOrganizerInvitation, \
    NotExistPendingOrganizerInvitation, UserNotIsOrganizerAndNotExistInvitation, AtLeastOneOrganizer
from app.exceptions.users_exceptions import UserNotFound
from app.repository.organizers_repository import OrganizerRepository
from app.repository.users_repository import UsersRepository
from app.schemas.members.member_schema import MemberRequestSchema, MemberResponseSchema
from app.schemas.users.user import UserSchema
from app.services.services import BaseService

INVITE_ORGANIZER_EXPIRATION_TIME = timedelta(days=20)


class EventOrganizersService(BaseService):
    def __init__(self, organizer_repository: OrganizerRepository, users_repository: UsersRepository):
        self.organizer_repository = organizer_repository
        self.users_repository = users_repository

    async def get_all_organizers(self, event_id: str) -> list[MemberResponseSchema]:
        users_organizers = await self.organizer_repository.get_all(event_id)
        return list(map(EventOrganizersService.__map_to_schema, users_organizers))

    async def get_all_chairs_by_status(self, event_id: str, status: InvitationStatus) -> list[MemberResponseSchema]:
        organizers_chairs = await self.organizer_repository.get_all_by_status(event_id, status)
        return list(map(EventOrganizersService.__map_to_schema, organizers_chairs))

    async def is_organizer(self, event_id: str, user_id: str) -> bool:
        organizer = await self.organizer_repository.get_organizer(event_id, user_id)
        return organizer is not None and organizer.invitation_status == InvitationStatus.ACCEPTED

    async def invite_organizer(self, organizer: MemberRequestSchema, event_id: str) -> str:
        user_id = await self.users_repository.get_user_id_by_email(organizer.email)
        if user_id is None:
            raise UserNotFound(organizer.email)
        invite_expiration_date = datetime.now() + INVITE_ORGANIZER_EXPIRATION_TIME
        if await self.organizer_repository.has_invitation_pending(event_id, user_id):
            return await self.organizer_repository.update_expiration_date(event_id, user_id, invite_expiration_date)
        await self.organizer_repository.create_organizer(
            event_id,
            user_id,
            expiration_date=invite_expiration_date
        )
        return user_id

    async def accept_organizer_invitation(self, user_id: str, event_id: str) -> None:
        if not await self.organizer_repository.has_invitation_pending(event_id, user_id):
            raise NotExistPendingOrganizerInvitation(event_id, user_id)
        chair = await self.organizer_repository.get_organizer(event_id, user_id)
        if chair.invitation_expiration_date < datetime.now():
            raise ExpiredOrganizerInvitation(event_id, user_id)
        await self.organizer_repository.accept_invitation(event_id, user_id)

    async def remove_organizer(self, event_id: str, user_id: str) -> None:
        if not await self.organizer_repository.has_invitation_or_is_member(event_id, user_id):
            raise UserNotIsOrganizerAndNotExistInvitation(event_id, user_id)
        users_organizers = await self.organizer_repository.get_all(event_id)
        if len(users_organizers) <= 1:
            raise AtLeastOneOrganizer(event_id, user_id)
        await self.organizer_repository.remove_member(event_id, user_id)

    @staticmethod
    def __map_to_schema(model: (UserModel, MemberModel)) -> MemberResponseSchema:
        user, organizer = model
        return MemberResponseSchema(
            event_id=organizer.event_id,
            user_id=organizer.user_id,
            invitation_date=organizer.creation_date,
            invitation_status=organizer.invitation_status,
            user=UserSchema(
                email=user.email,
                name=user.name,
                lastname=user.lastname
            )
        )
