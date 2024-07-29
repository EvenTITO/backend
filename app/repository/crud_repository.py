from pydantic import BaseModel
from sqlalchemy import and_, exists, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update


class Repository:
    """
    Base class for repositories
    """
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def _primary_key_conditions(self, id):
        return [self.model.id == id]

    async def exists(self, id) -> bool:
        conditions = await self._primary_key_conditions(id)
        return await self._exists_with_conditions(conditions)

    async def _exists_with_conditions(self, conditions):
        query = select(exists().where(and_(*conditions)))
        result = await self.session.execute(query)
        return result.scalar()

    async def get(self, id):
        conditions = await self._primary_key_conditions(id)
        return await self._get_with_conditions(conditions)

    async def _get_with_conditions(self, conditions):
        return await self._get_with_values(conditions, self.model)

    async def _get_with_values(self, conditions, values):
        query = select(values).where(and_(*conditions)).limit(1)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(self, id, object_update: BaseModel) -> bool:
        conditions = await self._primary_key_conditions(id)
        return await self._update_with_conditions(conditions, object_update)

    async def _update_with_conditions(self, conditions, object_update: BaseModel) -> bool:
        query = update(self.model).where(and_(*conditions)).values(object_update.model_dump(mode='json'))
        result = await self.session.execute(query)
        await self.session.commit()
        if result.rowcount < 1:
            return False
        return True

    async def _get_many_with_conditions(self, conditions, limit: int, offset: int):
        query = select(self.model).where(and_(*conditions)).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_many(self, limit: int, offset: int):
        query = select(self.model).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def _count_with_conditions(self, conditions):
        query = select(func.count()).where(and_(*conditions))
        result = await self.session.execute(query)
        return result.scalar_one()

    async def create(self, object_create: BaseModel):
        db_in = self.model(**object_create.model_dump(mode='json'))
        self.session.add(db_in)
        await self.session.commit()
        await self.session.refresh(db_in)
        return db_in

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
