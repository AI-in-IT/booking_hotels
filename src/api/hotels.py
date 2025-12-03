from typing import Annotated
from fastapi import Query, Body, APIRouter,Depends
from sqlalchemy import insert, select,func

from src.database import async_session_maker,engine

from schemas.hotels import Hotel, HotelPATCH
from models.hotels import HotelsOrm
from api.dependencies import PaginationDep
router = APIRouter(prefix="/hotels", tags = ["Отели"])



@router.get("", summary="Получение всех отелей")
async def get_hotels(
    pagination: PaginationDep,
    title:      str | None = Query(None, description="Название отеля"),
    location:   str | None = Query(None, description="Расположение отеля"),
    ):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))    
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))    

        
        
        query = (
            query
            .limit(per_page)
            .offset((pagination.page-1)*per_page)
            )

        print(query.compile(engine,compile_kwargs={"literal_binds":True}))

        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id : int ):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status" : "OK"}

@router.post("", summary="Добавление отеля")
async def creat_hotel(hotel_data : Hotel = Body(openapi_examples={
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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())

        print(add_hotel_stmt.compile(engine,compile_kwargs={"literal_binds":True}))

        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status" : "OK"}

@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
def put_hotel(hotel_id : int,hotel_data : Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name 
    return {"status" : "OK"}

@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле", description="Можно что-то одно прислать и мы в отель это перезапишем")
def patch_hotel(hotel_id : int, hotel_data : HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title: hotel["title"] = hotel_data.title
            if hotel_data.name: hotel["name"] = hotel_data.name  
    return {"status" : "OK"}


