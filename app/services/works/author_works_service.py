from datetime import datetime

from app.database.models.work import WorkStates, WorkModel
from app.exceptions.works.works_exceptions import TitleAlreadyExists, WorkNotFound, NotIsMyWork, \
    StatusNotAllowWorkUpdate, CannotUpdateWorkAfterDeadlineDate
from app.repository.works_repository import WorksRepository
from app.schemas.works.work import WorkSchema, WorkWithState
from app.services.services import BaseService
from app.services.works.works_service import WorksService


class AuthorWorksService(BaseService):
    def __init__(self, works_repository: WorksRepository, user_id: str, event_id: str, work_id: int):
        self.works_repository = works_repository
        self.user_id = user_id
        self.event_id = event_id
        self.work_id = work_id

    async def get_work(self) -> WorkWithState:
        my_work = await self.get_my_work()
        return WorksService.map_to_schema(my_work)

    async def get_my_work(self) -> WorkModel:
        my_work = await self.works_repository.get_work(event_id=self.event_id, work_id=self.work_id)
        if my_work is None:
            raise WorkNotFound(event_id=self.event_id, work_id=self.work_id)
        if my_work.author_id != self.user_id:
            raise NotIsMyWork(event_id=self.event_id, work_id=self.work_id)
        return my_work

    async def update_work(self, work_update: WorkSchema) -> None:
        await self.__validate_update_work()
        repeated_title = await self.works_repository.work_with_title_exists(self.event_id, work_update.title)
        if repeated_title:
            raise TitleAlreadyExists(work_update.title, self.event_id)
        await self.works_repository.update_work(work_update, self.event_id, self.work_id)

    async def __validate_update_work(self):
        work = await self.get_my_work()
        if work.state not in [WorkStates.SUBMITTED, WorkStates.RE_SUBMIT]:
            raise StatusNotAllowWorkUpdate(status=work.state, work_id=self.work_id)
        if datetime.today() > work.deadline_date:
            raise CannotUpdateWorkAfterDeadlineDate(deadline_date=work.deadline_date, work_id=self.work_id)
