from app.repository.works import WorksRepository
from app.services.works.exceptions.title_already_exists import TitleAlreadyExists
from datetime import datetime

from app.utils.services import BaseService


class WorksService(BaseService):
    def __init__(self, works_repository: WorksRepository, user_id: str, event_id: str):
        self.works_repository = works_repository
        self.user_id = user_id
        self.event_id = event_id

    async def create_work(self, work):
        deadline_date = datetime(2024, 11, 5)
        # TODO: use event deadline date.
        # TODO: validate before deadline.
        # TODO: validate tracks.
        repeated_title = await self.works_repository.work_with_title_exists(self.event_id, work.title)
        if repeated_title:
            raise TitleAlreadyExists(work.title, self.event_id)
        work = await self.works_repository.create(
            work,
            self.event_id,
            deadline_date,
            self.user_id
        )
        return work.id
