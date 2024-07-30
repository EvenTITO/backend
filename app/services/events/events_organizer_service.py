from app.repository.events_repository import EventsRepository
from app.services.services import BaseService


class EventsOrganizerService(BaseService):
    def __init__(self, events_repository: EventsRepository, event_id: str, user_id: str):
        self.events_repository = events_repository
        self.event_id = event_id
        self.user_id = user_id
