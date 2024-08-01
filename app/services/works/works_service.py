from datetime import datetime

from app.database.models.work import WorkModel
from app.exceptions.works.works_exceptions import TitleAlreadyExists
from app.repository.works_repository import WorksRepository
from app.schemas.works.work import WorkWithState
from app.services.services import BaseService


class WorksService(BaseService):
    def __init__(self, works_repository: WorksRepository, user_id: str, event_id: str):
        self.works_repository = works_repository
        self.user_id = user_id
        self.event_id = event_id

    async def get_all_event_works(self, offset: int, limit: int) -> list[WorkWithState]:
        works = await self.works_repository.get_all_works_for_event(self.event_id, offset, limit)
        return list(map(WorksService.map_to_schema, works))

    async def get_my_works(self, offset: int, limit: int) -> list[WorkWithState]:
        works = await self.works_repository.get_all_works_for_user(self.user_id, offset, limit)
        return list(map(WorksService.map_to_schema, works))

    async def create_work(self, work):
        deadline_date = datetime(2024, 11, 5)
        # TODO: use event deadline date.
        # TODO: validate before deadline.
        # TODO: validate tracks.
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

    @staticmethod
    def map_to_schema(model: WorkModel) -> WorkWithState:
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
