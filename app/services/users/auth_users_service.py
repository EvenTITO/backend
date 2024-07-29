from app.repository.users_repository import UsersRepository
from app.utils.services import BaseService


class AuthUsersService(BaseService):
    async def __init__(self, user_id: str, users_repository: UsersRepository):
        if not await users_repository.exists(user_id):
            raise Exception('no exists')
