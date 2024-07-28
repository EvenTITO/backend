from app.models.user import UserModel
from app.utils.crud_repository import CRUDBRepository


class UsersRepository(CRUDBRepository):
    model = UserModel
