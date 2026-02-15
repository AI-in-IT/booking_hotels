# from typing import Annotated
# from fastapi import Query, Body, APIRouter,Depends
# from sqlalchemy import insert, select,func

# from src.database import async_session_maker,engine

# from schemas.hotels import Hotel, HotelPATCH, HotelAdd
# from models.hotels import HotelsOrm
# from api.dependencies import PaginationDep



# from repositories.hotels import HotelsRepository

# router = APIRouter(prefix="/hotels", tags = ["Отели"])




from fastapi import APIRouter, Body
from schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest, RoomPut, RoomPutRequest
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
router = APIRouter(prefix="/hotels", tags = ["Номера"])


# @router.get("/all_rooms", summary="получение всех номеров")
# async def get_rooms_in_hotel():
#     async with async_session_maker() as session:
#         rooms = await RoomsRepository(session).get_all()
#     return rooms


@router.get("/{hotel_id}/rooms",summary="получение всех номеров конкретного отеля")
async def get_rooms_in_hotel(hotel_id:int):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_filtered(hotel_id=hotel_id)
    return rooms

@router.get("/{hotel_id}/rooms/{room_id}",summary="получение номера по ID номера и ID отеля")
async def get_room_in_hotel(hotel_id:int,room_id:int):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_filtered(hotel_id=hotel_id,id=room_id)
    return rooms

@router.post("/{hotel_id}/rooms", summary="добавление номера к отелю")
async def add_room(hotel_id:int, room_data : RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Эконом", "value":{
            "title" : "Эконом",
           "description" : "Базовый номер",
           "price" : 1000,
           "quantity" : 100,
        }},
    "2" : {
        "summary": "Комфорт", "value":{
           "title" : "Комфорт",
           "description" : "Роскошный номер",
           "price" : 2000,
           "quantity" : 20,
    }
        }})):
    
    # перевод  RoomPATCH в RoomAdd
    _room_data = RoomAdd(hotel_id =hotel_id, **room_data.model_dump())  
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status" : "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="удаление номера")
async def delete_room(hotel_id:int,room_id:int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id,hotel_id=hotel_id)
        await session.commit()
    return {"status" : "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение номера отеля")
async def put_room(hotel_id:int, room_id:int, room_data:RoomPutRequest):
    _room_data = RoomPut(hotel_id =hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data,id=room_id)
        await session.commit()
    return {"status" : "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="частичное изменение номера отеля")
async def patch_room(hotel_id:int, room_id:int, room_data:RoomPatchRequest):
    _room_data = RoomPatch(hotel_id =hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data,exclude_unset=True,id = room_id,hotel_id=hotel_id)
        await session.commit()
    return {"status" : "OK"}



