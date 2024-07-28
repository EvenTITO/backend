from app.repository.works import WorksRepository
from app.services.users.auth_users_service import AuthUsersService
from app.services.works.exceptions.title_already_exists import TitleAlreadyExists
from app.repository import works_crud
from datetime import datetime

from app.utils.services import BaseService


async def create_work(db, work, event_id, author_id):
    deadline_date = datetime(2024, 11, 5)
    # TODO: use event deadline date.
    repeated_title = await works_crud.work_with_title_exists(db, event_id, work.title)
    if repeated_title:
        raise TitleAlreadyExists(work.title, event_id)
    work = await works_crud.create_work(
        db,
        work,
        event_id,
        deadline_date,
        author_id
    )
    return work.id


class WorksService(BaseService):
    def __init__(self, works_repository: WorksRepository, user_id: str, event_id: str):
        self.works_repository = works_repository
        self.user_id = user_id
        self.event_id = event_id

    async def create_work(self, work):
        deadline_date = datetime(2024, 11, 5)
        # TODO: use event deadline date.
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
