from typing import List

from fastapi import APIRouter, Depends

from app.authorization.organizer_or_admin_dep import verify_is_organizer_or_admin
from app.schemas.members.member_schema import MemberRequestSchema, MemberResponseSchema
from app.schemas.members.member_schema import RolesRequestSchema
from app.services.event_members.event_members_service_dep import EventMembersServiceDep

event_members_router = APIRouter(
    prefix="/{event_id}/members",
    tags=["Events: Members"]
)


@event_members_router.get(
    path="",
    response_model=List[MemberResponseSchema],
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def read_event_members(members_service: EventMembersServiceDep, event_id: str):
    return await members_service.get_all_members(event_id)


@event_members_router.post(path="", status_code=201, dependencies=[Depends(verify_is_organizer_or_admin)])
async def invite_member(
        members_service: EventMembersServiceDep,
        member: MemberRequestSchema,
        event_id: str
) -> str:
    return await members_service.invite_member(member, event_id)


@event_members_router.delete(
    path="/{user_id}",
    status_code=201,
    response_model=None,
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def remove_member(
        event_id: str,
        user_id: str,
        member_service: EventMembersServiceDep
) -> None:
    await member_service.remove_member(event_id, user_id)


@event_members_router.put(
    path="/{user_id}/roles",
    status_code=201,
    response_model=None,
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def update(
        roles: RolesRequestSchema,
        event_id: str,
        user_id: str,
        member_service: EventMembersServiceDep
) -> None:
    await member_service.update_rol_member(event_id, user_id, roles)
