from app.database.models.member import MemberModel
from app.database.models.user import UserModel
from app.exceptions.members.organizer.organizer_exceptions import UserNotIsOrganizer, AtLeastOneOrganizer
from app.repository.organizers_repository import OrganizerRepository
from app.repository.users_repository import UsersRepository
from app.schemas.members.member_schema import MemberResponseSchema
from app.schemas.users.user import UserSchema
from app.services.services import BaseService


class EventOrganizersService(BaseService):
    def __init__(self, organizer_repository: OrganizerRepository, users_repository: UsersRepository):
        self.organizer_repository = organizer_repository
        self.users_repository = users_repository

    async def get_all_organizers(self, event_id: str) -> list[MemberResponseSchema]:
        users_organizers = await self.organizer_repository.get_all(event_id)
        return list(map(EventOrganizersService.__map_to_schema, users_organizers))

    async def is_organizer(self, event_id: str, user_id: str) -> bool:
        return await self.organizer_repository.is_member(event_id, user_id)

    async def remove_organizer(self, event_id: str, user_id: str) -> None:
        if not await self.organizer_repository.is_member(event_id, user_id):
            raise UserNotIsOrganizer(event_id, user_id)
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
            user=UserSchema(
                email=user.email,
                name=user.name,
                lastname=user.lastname
            )
        )
