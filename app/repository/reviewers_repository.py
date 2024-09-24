from uuid import UUID

from sqlalchemy import select, func, and_, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.reviewer import ReviewerModel
from app.database.models.user import UserModel
from app.repository.members_repository import MemberRepository
from app.schemas.members.reviewer_schema import ReviewerWithWorksResponseSchema, ReviewerResponseSchema, \
    ReviewerAssignmentSchema, ReviewerWithWorksDeadlineResponseSchema
from app.schemas.users.utils import UID


class ReviewerRepository(MemberRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ReviewerModel)

    def _primary_key_conditions(self, primary_key):
        event_id, reviewer_id, work_id = primary_key
        return [
            ReviewerModel.event_id == event_id,
            ReviewerModel.user_id == reviewer_id,
            ReviewerModel.work_id == work_id
        ]

    async def is_reviewer_of_work_in_event(self, event_id: UUID, user_id: UID, work_id: UUID) -> bool:
        return await self.exists((event_id, user_id, work_id))

    async def is_reviewer_in_event(self, event_id: UUID, user_id: UID) -> bool:
        query = (
            select(exists().where(and_(ReviewerModel.event_id == event_id, ReviewerModel.user_id == user_id)))
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all_reviewers(self, event_id: UUID, work_id: UUID | None)\
            -> list[ReviewerWithWorksDeadlineResponseSchema]:
        group_by_subquery = (
            select(
                ReviewerModel.event_id,
                ReviewerModel.user_id,
                ReviewerModel.review_deadline,
                func.array_agg(ReviewerModel.work_id).label('work_ids'),
            )
            .where(ReviewerModel.event_id == event_id)
            .group_by(ReviewerModel.event_id, ReviewerModel.user_id, ReviewerModel.review_deadline)
        )

        if work_id is not None:
            group_by_subquery = group_by_subquery.where(ReviewerModel.work_id == work_id)

        group_by_subquery = group_by_subquery.subquery()

        query = (
            select(
                group_by_subquery.c.event_id.label('event_id'),
                group_by_subquery.c.user_id.label('user_id'),
                group_by_subquery.c.work_ids.label('work_ids'),
                group_by_subquery.c.review_deadline.label('review_deadline'),
                UserModel
            )
            .join(UserModel, group_by_subquery.c.user_id == UserModel.id)
        )
        result = await self.session.execute(query)
        res = result.fetchall()
        return [
            ReviewerWithWorksDeadlineResponseSchema(
                event_id=row.event_id,
                work_ids=row.work_ids,
                user_id=row.user_id,
                review_deadline=row.review_deadline,
                user=row.UserModel)
            for row in res
        ]

    async def get_reviewer_by_user_id(self, event_id: UUID, user_id: UID) -> ReviewerWithWorksResponseSchema:
        group_by_subquery = (
            select(
                ReviewerModel.event_id,
                ReviewerModel.user_id,
                func.array_agg(ReviewerModel.work_id).label('work_ids'),
            )
            .where(and_(ReviewerModel.event_id == event_id, ReviewerModel.user_id == user_id))
            .group_by(ReviewerModel.event_id, ReviewerModel.user_id)
        )

        group_by_subquery = group_by_subquery.subquery()

        query = (
            select(
                group_by_subquery.c.event_id,
                group_by_subquery.c.user_id,
                group_by_subquery.c.work_ids,
                UserModel
            )
            .join(UserModel, group_by_subquery.c.user_id == UserModel.id)
        )
        result = await self.session.execute(query)
        res = result.fetchone()
        return ReviewerWithWorksResponseSchema(
            event_id=res.event_id, work_ids=res.work_ids, user_id=res.user_id, user=res.UserModel)

    async def get_reviewer_by_work_id(self, event_id: UUID, user_id: UID, work_id: UUID) -> ReviewerResponseSchema:
        query = select(UserModel, self.model).where(
            and_(
                self.model.event_id == event_id,
                self.model.user_id == user_id,
                self.model.work_id == work_id,
                self.model.user_id == UserModel.id
            )
        )
        result = await self.session.execute(query)
        user, model = result.fetchone()
        return ReviewerResponseSchema(
            event_id=model.event_id,
            work_id=model.work_id,
            user_id=model.user_id,
            review_deadline=model.review_deadline,
            user=user
        )

    async def create_reviewers(self, event_id: UUID, reviewers) -> None:
        for new_reviewer in reviewers:
            new_reviewer_model = ReviewerModel(
                event_id=event_id,
                work_id=new_reviewer.work_id,
                user_id=new_reviewer._user_id,
                review_deadline=new_reviewer.review_deadline,
            )
            self.session.add(new_reviewer_model)
        await self.session.commit()

    async def get_assignments(self, event_id: UUID, user_id: UID):
        query = (select(ReviewerModel.work_id, ReviewerModel.review_deadline)
                 .where(and_(ReviewerModel.event_id == event_id, ReviewerModel.user_id == user_id)))

        result = await self.session.execute(query)
        res = result.fetchall()
        return [ReviewerAssignmentSchema(work_id=row.work_id, review_deadline=row.review_deadline) for row in res]
