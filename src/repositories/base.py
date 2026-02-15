from sqlalchemy import insert, select,func,update,delete
from pydantic import BaseModel
from fastapi import HTTPException
from sqlalchemy.exc import MultipleResultsFound

from schemas.hotels import Hotel

class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self,session):
        self.session = session

    async def get_filtered(self, **filter_by):
       
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]


    async def get_all(self, *arg, **kwarg):
       
        query = select(self.model)
        result = await self.session.execute(query)
        return await self.get_filtered()
    


    async def get_one_or_none(self, **filter_by):
       
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)
    

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        
        try:
            existing = await self.get_one_or_none(**filter_by)
        except MultipleResultsFound:
            raise HTTPException(
                status_code=422, 
                detail="Найдено несколько отелей с таким ID"
            )
        if not existing:
            raise HTTPException(
                status_code=404, 
                detail="Отель не найден"
            )

        edit_data_stmt = (
        update(self.model)
        .values(**data.model_dump(exclude_unset=exclude_unset))
        .filter_by(**filter_by)
        )
        await self.session.execute(edit_data_stmt)
        
    async def delete(self, **filter_by) -> None:

        try:
            existing = await self.get_one_or_none(**filter_by)
        except MultipleResultsFound:
            raise HTTPException(
                status_code=422, 
                detail="Найдено несколько объектов с таким ID"
            )
        if not existing:
            raise HTTPException(
                status_code=404, 
                detail="Объект не найден"
            )

        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stmt)
        