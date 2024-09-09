from enum import Enum


class EventRole(str, Enum):
    ORGANIZER = "ORGANIZER"
    CHAIR = "CHAIR"
    REVIEWER = "REVIEWER"
    SPEAKER = "SPEAKER"
    ATTENDEE = "ATTENDEE"
