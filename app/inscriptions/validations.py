from app.repository import inscriptions_crud
from app.inscriptions.exceptions import InscriptionAlreadyExists
from app.events.utils import get_event


async def validate_inscription_not_exists(db, user_id, event_id):
    event = await get_event(db, event_id)
    if await inscriptions_crud.user_already_inscribed(db, user_id, event.id):
        raise InscriptionAlreadyExists(user_id, event_id)
