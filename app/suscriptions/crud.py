from app.utils.authorization import validate_user_permissions
from .model import SuscriptionModel
from sqlalchemy.orm import Session
from .schemas import (
    GetSuscriptionReplySchema,
    SuscriptionSchema
)
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException
import logging

EVENT_NOT_FOUND = "Event not found"
USER_NOT_FOUNT = "User not found"


def handle_database_suscription_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except IntegrityError as e:
            error_info = str(e.orig)
            if "id_event" in error_info.lower():
                raise HTTPException(status_code=409, detail=EVENT_NOT_FOUND)
            elif "id_suscriptor" in error_info.lower():
                raise HTTPException(status_code=409, detail=USER_NOT_FOUNT)
            else:
                logging.log(logging.ERROR, f"unexpected_error: {str(e)}")
                raise HTTPException(status_code=409, detail="Unexpected")
        except NoResultFound:
            raise HTTPException(status_code=404, detail=EVENT_NOT_FOUND)

    return wrapper


@handle_database_suscription_error
def suscribe_user_to_event(db: Session, suscription: SuscriptionSchema):
    db_suscription = SuscriptionModel(**suscription.model_dump())

    db.add(db_suscription)
    db.commit()
    db.refresh(db_suscription)

    return db_suscription


@handle_database_suscription_error
def read_event_suscriptions(db: Session, event_id: str):
    suscriptions = db \
        .query(SuscriptionModel) \
        .filter(
            SuscriptionModel.id_event == event_id
        ).all()

    suscriptions_dicts = [suscription.to_dict()
                          for suscription in suscriptions]
    return GetSuscriptionReplySchema(suscriptions=suscriptions_dicts)


@handle_database_suscription_error
def read_user_suscriptions(db: Session, user_id: str, caller_id: str):
    validate_user_permissions(db, caller_id, user_id=user_id)
    suscriptions = db \
        .query(SuscriptionModel) \
        .filter(
            SuscriptionModel.id_suscriptor == user_id
        ).all()

    suscriptions_dicts = [suscription.to_dict()
                          for suscription in suscriptions]
    return GetSuscriptionReplySchema(suscriptions=suscriptions_dicts)
