from typing import List

from fastapi import APIRouter
from uuid import UUID

from app.authorization.admin_user_dep import IsAdminUsrDep
from app.authorization.organizer_dep import IsOrganizerDep
from app.authorization.util_dep import or_
from app.schemas.members.member_schema import MemberRequestSchema, MemberResponseSchema
from app.schemas.members.member_schema import RolesRequestSchema
from app.schemas.users.utils import UID
from app.services.event_members.event_members_service_dep import EventMembersServiceDep

event_members_router = APIRouter(
    prefix="/{event_id}/members",
    tags=["Events: Members"]
)


@event_members_router.get(
    path="",
    response_model=List[MemberResponseSchema],
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)]
)
async def read_event_members(members_service: EventMembersServiceDep, event_id: UUID):
    return await members_service.get_all_members(event_id)


@event_members_router.post(path="", status_code=201, dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)])
async def invite_member(
        members_service: EventMembersServiceDep,
        member: MemberRequestSchema,
        event_id: UUID
) -> UID:
    return await members_service.invite_member(member, event_id)


@event_members_router.delete(
    path="/{user_id}",
    status_code=201,
    response_model=None,
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)]
)
async def remove_member(
        event_id: UUID,
        user_id: UID,
        member_service: EventMembersServiceDep
) -> None:
    await member_service.remove_member(event_id, user_id)


@event_members_router.put(
    path="/{user_id}/roles",
    status_code=201,
    response_model=None,
    dependencies=[or_(IsOrganizerDep, IsAdminUsrDep)]
)
async def update(
        roles: RolesRequestSchema,
        event_id: UUID,
        user_id: UID,
        member_service: EventMembersServiceDep
) -> None:
    await member_service.update_rol_member(event_id, user_id, roles)
