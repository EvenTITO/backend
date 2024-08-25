from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.reviewer import ReviewerModel
from app.repository.members_repository import MemberRepository


class ReviewerRepository(MemberRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ReviewerModel)

    def _primary_key_conditions(self, primary_key):
        event_id, chair_id, work_id = primary_key
        return [
            ReviewerModel.event_id == event_id,
            ReviewerModel.user_id == chair_id,
            ReviewerModel.work_id == work_id
        ]
