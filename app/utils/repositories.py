class BaseRepository:
    """
    Base class for repositories
    """

    def __init__(self, session):
        self._session = session

    @property
    def session(self):
        return self._session
