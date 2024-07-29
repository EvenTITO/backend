from pydantic import BaseModel
from sqlalchemy import and_, exists
from app.utils.repositories import BaseRepository
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update


class CRUDBRepository(BaseRepository):
    def __init__(self, session: AsyncSession, model):
        super().__init__(session)
        self.model = model

    async def exists(self, id) -> bool:
        conditions = [self.model.id == id]
        return self._exists_with_conditions(conditions)

    async def _exists_with_conditions(self, conditions):
        query = select(exists().where(and_(*conditions)))
        result = await self.session.execute(query)
        return result.scalar()

    async def get(self, id):
        conditions = [self.model.id == id]
        return self._get_with_conditions(conditions)

    async def _get_with_conditions(self, conditions):
        query = select(self.model).where(and_(*conditions))
        result = await self.session.execute(query)
        return result.scalars().first()

    async def _update_with_conditions(self, conditions, object_update: BaseModel) -> bool:
        query = update(self.model).where(and_(*conditions)).values(object_update.model_dump(mode='json'))
        result = await self.session.execute(query)
        await self.session.commit()
        if result.rowcount < 1:
            return False
        return True

    # def get(self, id):
    #     return self.session.query(self.model).filter(self.model.id == id).first()

    # def get_multi(self, skip=0, limit=100):
    #     return self.session.query(self.model).offset(skip).limit(limit).all()

    # def create(self, obj_in):
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data)
    #     self.session.add(db_obj)
    #     self.session.commit()
    #     self.session.refresh(db_obj)
    #     return db_obj

    # def update(self, db_obj, obj_in):
    #     obj_data = jsonable_encoder(db_obj)
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     for field in obj_data:
    #         if field in update_data:
    #             setattr(db_obj, field, update_data[field])
    #     self.session.add(db_obj)
    #     self.session.commit()
    #     self.session.refresh(db_obj)
    #     return db_obj

    # def remove(self, id):
    #     obj = self.session.query(self.model).get(id)
    #     self.session.delete(obj)
    #     self.session.commit()
    #     return obj
