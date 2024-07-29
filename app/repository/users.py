from app.models.user import UserModel, UserRole
from app.utils.crud_repository import CRUDBRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UsersRepository(CRUDBRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)

    async def get_amount_admins(self):
        admin_role = UserRole.ADMIN.value
        conditions = [UserModel.role == admin_role]
        return await self._count_with_conditions(conditions)
