from datetime import datetime

from app.database.models.work import WorkModel, WorkStates
from app.exceptions.works.works_exceptions import TitleAlreadyExists, StatusNotAllowWorkUpdate, \
    CannotUpdateWorkAfterDeadlineDate, WorkNotFound, NotIsMyWork
from app.repository.works_repository import WorksRepository
from app.schemas.works.work import WorkWithState, WorkSchema
from app.services.services import BaseService


class WorksService(BaseService):
    def __init__(self, works_repository: WorksRepository, user_id: str, event_id: str):
        self.works_repository = works_repository
        self.user_id = user_id
        self.event_id = event_id

    async def get_all_event_works(self, track: str, offset: int, limit: int) -> list[WorkWithState]:
        if track:
            works = await self.works_repository.get_all_event_works_for_track(self.event_id, track, offset, limit)
        else:
            works = await self.works_repository.get_all_works_for_event(self.event_id, offset, limit)
        return list(map(WorksService.__map_to_schema, works))

    async def get_my_works(self, offset: int, limit: int) -> list[WorkWithState]:
        works = await self.works_repository.get_all_works_for_user(self.user_id, offset, limit)
        return list(map(WorksService.__map_to_schema, works))

    async def create_work(self, work: WorkSchema) -> int:
        deadline_date = datetime(2024, 11, 5)
        # TODO: use event deadline date.
        # TODO: validate before deadline.
        # TODO: validate track.
        repeated_title = await self.works_repository.work_with_title_exists(self.event_id, work.title)
        if repeated_title:
            raise TitleAlreadyExists(work.title, self.event_id)
        work = await self.works_repository.create_work(
            work,
            self.event_id,
            deadline_date,
            self.user_id
        )
        return work.id

    async def is_my_work(self, caller_id: str, event_id: str, work_id: str) -> bool:
        work = await self.__get_work(event_id, work_id)
        return work.author_id == caller_id

    async def get_work(self, work_id: str) -> WorkWithState:
        work = await self.__get_work(self.event_id, work_id)
        return WorksService.__map_to_schema(work)

    async def update_work(self, work_id: str, work_update: WorkSchema) -> None:
        await self.validate_update_work(work_id)
        repeated_title = await self.works_repository.work_with_title_exists(self.event_id, work_update.title)
        if repeated_title:
            raise TitleAlreadyExists(work_update.title, self.event_id)
        await self.works_repository.update_work(work_update, self.event_id, int(work_id))

    async def validate_update_work(self, work_id: str) -> None:
        my_work = await self.__get_my_work(work_id)
        if my_work.state not in [WorkStates.SUBMITTED, WorkStates.RE_SUBMIT]:
            raise StatusNotAllowWorkUpdate(status=my_work.state, work_id=work_id)
        if datetime.today() > my_work.deadline_date:
            raise CannotUpdateWorkAfterDeadlineDate(deadline_date=my_work.deadline_date, work_id=work_id)

    async def __get_my_work(self, work_id: str) -> WorkModel:
        work = await self.__get_work(self.event_id, work_id)
        if work.author_id != self.user_id:
            raise NotIsMyWork(event_id=self.event_id, work_id=work_id)
        return work

    async def __get_work(self, event_id: str, work_id: str) -> WorkModel:
        work = await self.works_repository.get_work(event_id=event_id, work_id=int(work_id))
        if work is None:
            raise WorkNotFound(event_id=event_id, work_id=work_id)
        return work

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
            authors=model.authors
        )
