
from fastapi import APIRouter, Body
from schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest, RoomPut, RoomPutRequest
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository

from api.dependencies import DBDep


router = APIRouter(prefix="/hotels", tags = ["Номера"])

@router.get("/{hotel_id}/rooms",summary="получение всех номеров конкретного отеля")
async def get_rooms_in_hotel(db: DBDep,hotel_id:int):

    rooms = await db.rooms.get_filtered(hotel_id=hotel_id)
    return rooms

@router.get("/{hotel_id}/rooms/{room_id}",summary="получение номера по ID номера и ID отеля")
async def get_room_in_hotel(db: DBDep,hotel_id:int,room_id:int):
    rooms = await db.rooms.get_filtered(hotel_id=hotel_id,id=room_id)
    return rooms


@router.post("/{hotel_id}/rooms", summary="добавление номера к отелю")
async def add_room(db: DBDep,hotel_id:int, room_data : RoomAddRequest = Body(openapi_examples={
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
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status" : "OK", "data": room}
    

@router.delete("/{hotel_id}/rooms/{room_id}", summary="удаление номера")
async def delete_room(db: DBDep,hotel_id:int,room_id:int):

    await db.rooms.delete(id=room_id,hotel_id=hotel_id)
    await db.commit()
    return {"status" : "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение номера отеля")
async def put_room(db: DBDep,hotel_id:int, room_id:int, room_data:RoomPutRequest):
    _room_data = RoomPut(hotel_id =hotel_id, **room_data.model_dump())
    
    await db.rooms.edit(_room_data,id=room_id)
    await db.commit()

    return {"status" : "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="частичное изменение номера отеля")
async def patch_room(db: DBDep,hotel_id:int, room_id:int, room_data:RoomPatchRequest):
    _room_data = RoomPatch(hotel_id =hotel_id, **room_data.model_dump(exclude_unset=True))

    await db.rooms.edit(_room_data,exclude_unset=True,id = room_id,hotel_id=hotel_id)
    await db.commit()

    return {"status" : "OK"}



