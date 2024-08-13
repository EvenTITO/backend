from datetime import datetime

from sqlalchemy import func, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.submission import SubmissionModel
from app.repository.crud_repository import Repository


class SubmissionsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, SubmissionModel)

    async def get_last_submission(self, event_id, work_id) -> SubmissionModel:
        return await self._get_with_conditions(
            and_(
                self.model.event_id == event_id,
                self.model.work_id == work_id,
                func.max(self.model.id)
            ))

    async def do_new_submit(self, event_id, work_id) -> SubmissionModel:
        new_submission = SubmissionModel(event_id=event_id, work_id=work_id)
        return await self._create(new_submission)

    async def update_submit(self, event_id, work_id) -> SubmissionModel:
        last_submission = await self.get_last_submission(event_id, work_id)
        if last_submission is None:
            return await self.do_new_submit(event_id, work_id)
        update_query = (
            update(self.model).where(self.model.id == last_submission.id).values(last_update=datetime.now())
        )
        await self.session.execute(update_query)
        await self.session.commit()
        return last_submission
