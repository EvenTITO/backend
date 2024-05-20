from sqlalchemy.orm import Session
from app.users.model import UserModel


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).one()
