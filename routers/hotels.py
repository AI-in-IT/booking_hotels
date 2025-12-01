from typing import Annotated
from fastapi import Query, Body, APIRouter,Depends
from schemas.hotels import Hotel, HotelPATCH
from dependencies import PaginationDep
router = APIRouter(prefix="/hotels", tags = ["Отели"])




hotels = [
    {"id":1, "title": "Сочинский пацык", "name": "Sochi boy"},
    {"id":2, "title": "Дубайский шейх", "name": "Dubai sheih"},
    {"id":3, "title": "Жуковский инженер", "name": "Zukovski enginer"},
    {"id":4, "title": "Ахтубинский летчик", "name": "Ahtubinsk flyer"},
    {"id":5, "title": "Бронницкий ювелир", "name": "Bronnic jewel"},
    {"id":6, "title": "Казанский репер", "name": "Kazan reper"},
]


@router.get("", summary="Получение всех отелей")
def get_hotels(
    pagination: PaginationDep,
    id:     int | None = Query(None, description="Айдишник отеля"), 
    title:  str | None = Query(None, description="Название отеля"),
    ):
    result = []
    for hotel in hotels:
        if id: 
            if hotel["id"]!=id:
                continue
        if title:
            if hotel["title"]!=title:
                continue
        result.append(hotel)
    if pagination.page and pagination.per_page:
        return result[(pagination.page-1)*pagination.per_page:][:pagination.per_page]
    else:
        return result

@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id : int ):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status" : "OK"}

@router.post("", summary="Добавление отеля")
def creat_hotel(hotel_data : Hotel = Body(openapi_examples={
    "1": {
        "summary": "Москва", "value":{
           "title" : "Московский барин",
           "name" : "Moscow Barin" 
        }},
    "2" : {
        "summary": "Питер", "value":{
           "title" : "Питерский солеварец",
           "name" : "Piter Solter" 
    }
        }})):
    global hotels
    hotels.append({"id" : hotels[-1]["id"]+1, "title" : hotel_data.title, "name" : hotel_data.name})
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


