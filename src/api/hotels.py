from typing import Annotated
from fastapi import Query, Body, APIRouter,Depends
from sqlalchemy import insert, select,func

from src.database import async_session_maker,engine

from schemas.hotels import Hotel, HotelPATCH, HotelAdd
from models.hotels import HotelsOrm
from api.dependencies import PaginationDep

from repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags = ["Отели"])



@router.get("", summary="Получение всех отелей")
async def get_hotels(
    pagination: PaginationDep,
    title:      str | None = Query(None, description="Название отеля"),
    location:   str | None = Query(None, description="Расположение отеля"),
    ):
    
    per_page = pagination.per_page or 5
    
    async with async_session_maker() as session:
        
        return await HotelsRepository(session).get_all(location = location,
                                                       title = title,
                                                       limit = per_page, 
                                                       offset = (pagination.page-1)*per_page)
        

@router.get("/{hotel_id}",summary="получение отеля по id")
async def get_hotel(hotel_id:int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
    return hotel

@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id : int ):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id = hotel_id)
        await session.commit()
    return {"status" : "OK"}

@router.post("", summary="Добавление отеля")
async def creat_hotel(hotel_data : HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Москва", "value":{
           "title" : "Московский барин",
           "location" : "Москва ул. Кремлевская 8 " 
        }},
    "2" : {
        "summary": "Питер", "value":{
           "title" : "Питерский солеварец",
           "location" : "Питер ул. Невская 4" 
    }
        }})):

    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status" : "OK", "data": hotel}

@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
async def put_hotel(hotel_id : int,hotel_data : HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data,id = hotel_id)
        await session.commit()
    return {"status" : "OK"}

@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле", description="Можно что-то одно прислать и мы в отель это перезапишем")
async def patch_hotel(hotel_id : int, hotel_data : HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data,exclude_unset=True,id = hotel_id)
        await session.commit()
    return {"status" : "OK"}


