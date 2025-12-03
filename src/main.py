#импортируем нужные библиотеки
from fastapi import FastAPI
import uvicorn

#настройки для того, чтобы питон увидел src
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


#импортируем необходимые роутеры
from src.api.hotels import router as router_hotels
from src.api.docs import create_docs_router
from _course_helpers.fastapi_load_test import router as router_tests


#импортируем переменные окружения из файла .env
from src.config import settings

#импортируем файл с БД
from src.database import *

#создаем экземпляр приложения fastapi
app = FastAPI(docs_url=None, redoc_url=None) 

#создаем роутер для ручек документации
router_docs = create_docs_router(app) 


#подключаем все роутеры к нашему приложению
app.include_router(router_hotels)
app.include_router(router_docs)
app.include_router(router_tests)



#Запускаем наше приложение 
if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload = True )