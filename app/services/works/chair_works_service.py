from app.repository.works import WorksRepository

from app.utils.services import BaseService


class ChairWorksService(BaseService):
    def __init__(self, works_repository: WorksRepository, user_id: str, event_id: str):
        self.works_repository = works_repository
        self.user_id = user_id
        self.event_id = event_id
        # TODO: validate I am CHAIR.

    async def get_works_in_my_tracks(self, limit: int = 100, offset: int = 0):
        my_tracks = ['math', 'chemistry']
        # TODO: Get my tracks.
        works = await self.works_repository.get_works_in_tracks(self.event_id, my_tracks, limit, offset)
        return works

    async def assign_work_to_reviewer(self, work_id: int, reviewer_id: str):
        pass
