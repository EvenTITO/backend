from datetime import datetime
from uuid import UUID

from app.database.models.inscription import InscriptionRole
from app.database.models.work import WorkModel, WorkStates
from app.exceptions.works.works_exceptions import TitleAlreadyExists, StatusNotAllowWorkUpdate, \
    CannotUpdateWorkAfterDeadlineDate, WorkNotFound, NotIsMyWork, CannotCreateWorkAfterDeadlineDate, \
    TrackNotExistInEvent, CannotCreateWorkIfNotSpeakerInscription
from app.repository.works_repository import WorksRepository
from app.schemas.events.dates import MandatoryDates
from app.schemas.users.utils import UID
from app.schemas.works.work import WorkWithState, WorkSchema, WorkStateSchema
from app.services.event_inscriptions.event_inscriptions_service import EventInscriptionsService
from app.services.events.events_configuration_service import EventsConfigurationService
from app.services.notifications.events_notifications_service import EventsNotificationsService
from app.services.services import BaseService


class WorksService(BaseService):
    def __init__(
            self,
            user_id: UID,
            event_id: UUID,
            event_configuration_service: EventsConfigurationService,
            event_notification_service: EventsNotificationsService,
            inscription_service: EventInscriptionsService,
            works_repository: WorksRepository
    ):
        self.user_id = user_id
        self.event_id = event_id
        self.event_configuration_service = event_configuration_service
        self.inscription_service = inscription_service
        self.works_repository = works_repository
        self.event_notification_service = event_notification_service

    async def get_works(self, track: str, offset: int, limit: int) -> list[WorkWithState]:
        if track:
            works = await self.works_repository.get_works_by_track(self.event_id, track, offset, limit)
        else:
            works = await self.works_repository.get_all_works_for_event(self.event_id, offset, limit)
        return list(map(WorksService.__map_to_schema, works))

    async def get_my_works(self, offset: int, limit: int) -> list[WorkWithState]:
        works = await self.works_repository.get_all_works_for_user(self.user_id, offset, limit)
        return list(map(WorksService.__map_to_schema, works))

    async def create_work(self, work: WorkSchema) -> UUID:
        submission_deadline = await self._get_submission_deadline()
        if submission_deadline.date < datetime.now().date():
            raise CannotCreateWorkAfterDeadlineDate(submission_deadline)

        repeated_title = await self.works_repository.work_with_title_exists(self.event_id, work.title)
        if repeated_title:
            raise TitleAlreadyExists(work.title, self.event_id)

        event_tracks = await self.event_configuration_service.get_event_tracks()
        if work.track not in event_tracks:
            raise TrackNotExistInEvent(self.event_id, work.track)

        my_inscriptions = await self.inscription_service.get_my_event_inscriptions(0, 100)
        has_inscription = True in (InscriptionRole.SPEAKER in inscription.roles for inscription in my_inscriptions)
        if not has_inscription:
            raise CannotCreateWorkIfNotSpeakerInscription(self.event_id)

        work = await self.works_repository.create_work(
            work,
            self.event_id,
            datetime.combine(submission_deadline.date, submission_deadline.time),
            self.user_id
        )
        return work.id

    async def is_my_work(self, caller_id: UID, work_id: UUID) -> bool:
        work = await self.__get_work(self.event_id, work_id)
        return work.author_id == caller_id

    async def get_work(self, work_id: UUID) -> WorkWithState:
        work = await self.__get_work(self.event_id, work_id)
        return WorksService.__map_to_schema(work)

    async def update_work(self, work_id: UUID, work_update: WorkSchema) -> None:
        await self.validate_update_work(work_id)
        # TODO: ok remove ?
        # repeated_title = await self.works_repository.work_with_title_exists(self.event_id, work_update.title)
        # if repeated_title:
        #     raise TitleAlreadyExists(work_update.title, self.event_id)
        await self.works_repository.update_work(work_update, self.event_id, work_id)

    async def update_work_status(self, work_id: UUID, status: WorkStateSchema) -> None:
        if not await self.exist_work(work_id):
            raise WorkNotFound(event_id=self.event_id, work_id=work_id)
        await self.works_repository.update_work_status(self.event_id, work_id, status)
        work = await self.works_repository.get_work(self.event_id, work_id)
        await self.event_notification_service.notify_change_work_status(
            self.event_id,
            self.user_id,
            {"id": work_id, "work": work},
            status.state)

    async def validate_update_work(self, work_id: UUID) -> None:
        my_work = await self.__get_my_work(work_id)
        if my_work.state not in [WorkStates.SUBMITTED, WorkStates.RE_SUBMIT]:
            raise StatusNotAllowWorkUpdate(status=my_work.state, work_id=work_id)
        if datetime.today() > my_work.deadline_date:
            raise CannotUpdateWorkAfterDeadlineDate(deadline_date=my_work.deadline_date, work_id=work_id)

    async def __get_my_work(self, work_id: UUID) -> WorkModel:
        work = await self.__get_work(self.event_id, work_id)
        if work.author_id != self.user_id:
            raise NotIsMyWork(event_id=self.event_id, work_id=work_id)
        return work

    async def __get_work(self, event_id: UUID, work_id: UUID) -> WorkModel:
        if not await self.exist_work(work_id):
            raise WorkNotFound(event_id=self.event_id, work_id=work_id)
        return await self.works_repository.get_work(event_id=event_id, work_id=work_id)

    async def exist_work(self, work_id: UUID) -> bool:
        return await self.works_repository.exists_work(self.event_id, work_id)

    async def _get_submission_deadline(self):
        dates_schema = await self.event_configuration_service.get_dates()
        return next((x for x in dates_schema.dates if x.name == MandatoryDates.SUBMISSION_DEADLINE_DATE), None)

    @staticmethod
    def __map_to_schema(model: WorkModel) -> WorkWithState:
        return WorkWithState(
            id=model.id,
            state=model.state,
            deadline_date=model.deadline_date,
            title=model.title,
            track=model.track,
            abstract=model.abstract,
            keywords=model.keywords,
            authors=model.authors,
            talk=model.talk
        )
