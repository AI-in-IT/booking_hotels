from fastapi import Query, Body, APIRouter,Depends


from schemas.hotels import HotelPATCH, HotelAdd

from api.dependencies import DBDep, PaginationDep


router = APIRouter(prefix="/hotels", tags = ["Отели"])



@router.get("", summary="Получение всех отелей")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title:      str | None = Query(None, description="Название отеля"),
    location:   str | None = Query(None, description="Расположение отеля"),
    ):
    
    per_page = pagination.per_page or 5
    

    return await db.hotels.get_all(location = location,
                                                       title = title,
                                                       limit = per_page, 
                                                       offset = (pagination.page-1)*per_page)
        

@router.get("/{hotel_id}",summary="получение отеля по id")
async def get_hotel(db: DBDep,hotel_id:int):
    return await db.hotels.get_one_or_none(id=hotel_id)

@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(db: DBDep,hotel_id : int ):
    await db.hotels.delete(id = hotel_id)
    await db.commit()
    return {"status" : "OK"}


@router.post("", summary="Добавление отеля")
async def creat_hotel(db: DBDep,hotel_data : HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status" : "OK", "data": hotel}

@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
async def put_hotel(db: DBDep,hotel_id : int,hotel_data : HotelAdd):
    await db.hotels.edit(hotel_data,id = hotel_id)
    await db.commit()
    return {"status" : "OK"}

@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле", description="Можно что-то одно прислать и мы в отель это перезапишем")
async def patch_hotel(db: DBDep,hotel_id : int, hotel_data : HotelPATCH):
    await db.hotels.edit(hotel_data,exclude_unset=True,id = hotel_id)
    await db.commit()
    return {"status" : "OK"}


