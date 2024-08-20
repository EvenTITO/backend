from functools import reduce
from itertools import groupby
from operator import itemgetter

from app.database.models.member import MemberModel
from app.database.models.user import UserModel
from app.exceptions.members.organizer.organizer_exceptions import AlreadyOrganizerExist, AtLeastOneOrganizer
from app.exceptions.users_exceptions import UserNotFound
from app.repository.chairs_repository import ChairRepository
from app.repository.organizers_repository import OrganizerRepository
from app.repository.users_repository import UsersRepository
from app.schemas.members.member_schema import MemberRequestSchema, MemberResponseSchema, MemberResponseWithRolesSchema
from app.schemas.users.user import UserSchema
from app.services.services import BaseService


class EventMembersService(BaseService):
    def __init__(
            self,
            organizer_repository: OrganizerRepository,
            chair_repository: ChairRepository,
            users_repository: UsersRepository,
    ):
        self.users_repository = users_repository
        self.repositories = {"organizer": organizer_repository, "chair": chair_repository}

    async def get_all_members(self, event_id: str) -> set[MemberResponseSchema]:
        result = []
        for role, repository in self.repositories.items():
            members = await repository.get_all(event_id)
            result += list(map(lambda x: EventMembersService.__map_to_schema(x, role), members))
        members_response = {
            MemberResponseWithRolesSchema(
                **v[0].model_dump(mode='json'), roles=list(reduce(lambda x, y: x.roles + y.roles, v)))
            for k, v in groupby(result, key=itemgetter('user_id'))
        }
        return members_response

    async def is_member(self, event_id: str, user_id: str) -> bool:
        for role, repository in self.repositories.items():
            if await repository.is_member(event_id, user_id):
                return True
        return False

    async def invite_member(self, member: MemberRequestSchema, event_id: str) -> str:
        user_id = await self.users_repository.get_user_id_by_email(member.email)
        if user_id is None:
            raise UserNotFound(member.email)
        member_repository = self.repositories[member.role]
        if await member_repository.is_member(event_id, user_id):
            raise AlreadyOrganizerExist(event_id, user_id)
        await member_repository.create_member(event_id, user_id)
        return user_id

    async def remove_member(self, event_id: str, user_id: str) -> None:
        for role, repository in self.repositories.items():
            if await repository.is_member(event_id, user_id):
                if role == "organizer":
                    users_organizers = await repository.get_all(event_id)
                    if len(users_organizers) <= 1:
                        continue
                await repository.remove_member(event_id, user_id)

    @staticmethod
    def __map_to_schema(model: (UserModel, MemberModel), rol: str) -> MemberResponseWithRolesSchema:
        user, organizer = model
        return MemberResponseWithRolesSchema(
            event_id=organizer.event_id,
            user_id=organizer.user_id,
            roles=[rol],
            user=UserSchema(
                email=user.email,
                name=user.name,
                lastname=user.lastname
            )
        )
