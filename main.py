#импортируем нужные библиотеки
from fastapi import FastAPI
import uvicorn
#импортируем необходимые роутеры
from routers.hotels import router as router_hotels
from routers.docs import create_docs_router
from _course_helpers.fastapi_load_test import router as router_tests


app = FastAPI(docs_url=None, redoc_url=None) 

router_docs = create_docs_router(app) #создается роутер для ручек документации


#подключаем все роутеры к нашему приложению
app.include_router(router_hotels)
app.include_router(router_docs)
app.include_router(router_tests)



#Запускаем наше приложение 
if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload = True )