from app.models.user import UserModel, UserRole
from app.schemas.users.user import UserSchema
from app.utils.crud_repository import CRUDBRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UsersRepository(CRUDBRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)

    async def get_amount_admins(self):
        admin_role = UserRole.ADMIN.value
        conditions = [UserModel.role == admin_role]
        return await self._count_with_conditions(conditions)

    async def get_user_by_email(self, email):
        conditions = [UserModel.email == email]
        return await self._get_with_conditions(conditions)

    async def create_user(self, id, user: UserSchema):
        db_user = UserModel(**user.model_dump(), id=id)
        return await self._create(db_user)
