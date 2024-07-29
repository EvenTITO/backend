from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """
    Base class for repositories
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    @property
    def session(self):
        return self._session
