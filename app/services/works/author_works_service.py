from app.repository.works import WorksRepository
from app.schemas.works.work import WorkSchema, WorkWithState
from app.utils.services import BaseService


class AuthorWorksService(BaseService):
    def __init__(self, works_repository: WorksRepository, user_id: str, event_id: str, work_id: int):
        self.works_repository = works_repository
        self.user_id = user_id
        self.event_id = event_id
        self.work_id = work_id

    async def get_work(self) -> WorkWithState:
        my_work = await self.works_repository.get_work(event_id=self.event_id, work_id=self.work_id)

        if my_work is None:
            raise Exception('None work')

        if my_work.id_author != self.user_id:
            raise Exception('Not my work')
        # TODO: tambien deberia poder traerlo si soy reviewer org o chair del track.

        return my_work

    async def update(work_update: WorkSchema):
        pass
