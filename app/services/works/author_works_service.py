from app.repository.works import WorksRepository
from app.schemas.works.work import BasicWorkInfoForAuthor, WorkSchema, WorkWithState
from app.schemas.works.work_stages import BeforeDeadline
from app.utils.services import BaseService
from datetime import datetime


class AuthorWorksService(BaseService):
    def __init__(self, works_repository: WorksRepository, user_id: str, event_id: str, work_id: int):
        self.works_repository = works_repository
        self.user_id = user_id
        self.event_id = event_id
        self.work_id = work_id

    async def get_work(self) -> WorkWithState:
        my_work = await self.works_repository.get_work(event_id=self.event_id, work_id=self.work_id)
        # print(WorkSchema.model_validate(my_work).model_dump())
        if my_work is None:
            raise Exception('None work')
        if my_work.id_author != self.user_id:
            raise Exception('Not my work')
        work = WorkSchema.model_validate(obj=my_work)
        stage = BeforeDeadline(
            deadline_date=datetime.today()

        )
        return WorkWithState(
            **work.model_dump(),
            state=stage
        )

        return my_work
        stage = "no deadline"
        last_submission = works_repository.get_last_submission(event_id=self.event_id, work_id=self.work_id)
        if last_submission == None:
            if my_work.submission_date < today:
                stage = "waiting deadline"
            else:
                stage = "waiting decision"

        return BasicWorkInfoForAuthor
