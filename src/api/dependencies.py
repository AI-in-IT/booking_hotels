from typing import Annotated
from fastapi import HTTPException, Query, Depends, Request
from pydantic import BaseModel

from services.auth import AuthService
from utils.db_manager import DBManager

from src.database import async_session_maker

class PaginationParams(BaseModel):
    page:     Annotated[int | None, Query(1, ge = 1)]
    per_page: Annotated[int | None, Query(None, ge = 1, le = 30)]




PaginationDep = Annotated[PaginationParams, Depends()]










def get_token(request: Request):
    try:
            return request.cookies["access_token"]
    except:
            raise HTTPException(status_code=401, detail="Нет токена")
    


def get_current_user_id(access_token: str = Depends(get_token)):

    access_token_decode = AuthService().decode_token(access_token)
    user_id = access_token_decode["user_id"]
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
      async with DBManager(session_factory=async_session_maker) as db:
            yield db

DBDep = Annotated[DBManager, Depends(get_db)]