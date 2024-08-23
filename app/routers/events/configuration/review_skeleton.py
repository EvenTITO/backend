from fastapi import APIRouter, Depends
from app.authorization.user_id_dep import verify_user_exists
from app.schemas.events.review_skeleton.review_skeleton import ReviewSkeletonSchema
from app.authorization.organizer_or_admin_dep import verify_is_organizer_or_admin
from app.services.events.events_configuration_service_dep import EventsConfigurationServiceDep

review_skeleton_configuration_router = APIRouter(prefix="/review-skeleton")


@review_skeleton_configuration_router.put(
    "",
    status_code=204,
    response_model=None,
    dependencies=[Depends(verify_is_organizer_or_admin)]
)
async def change_review_skeleton(
    review_skeleton: ReviewSkeletonSchema,
    events_configuration_service: EventsConfigurationServiceDep,
):
    await events_configuration_service.update_review_skeleton(review_skeleton)


@review_skeleton_configuration_router.get("", status_code=200, dependencies=[Depends(verify_user_exists)])
async def get_review_skeleton(
    events_configuration_service: EventsConfigurationServiceDep,
) -> ReviewSkeletonSchema:
    res = await events_configuration_service.get_review_skeleton()
    return res
