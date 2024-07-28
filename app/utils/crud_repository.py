from fastapi.encoders import jsonable_encoder
from sqlalchemy import exists
from app.utils.repositories import BaseRepository
from sqlalchemy.future import select


class CRUDBRepository(BaseRepository):
    model = None

    async def exists(self, id) -> bool:
        query = select(exists().where(self.model.id == id))
        result = await self.session.execute(query)
        return result.scalar()

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
