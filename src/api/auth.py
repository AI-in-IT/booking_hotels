
from fastapi import APIRouter, HTTPException, Request, Response
from api.dependencies import UserIdDep
from repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd, UserWithHashedPassword
from src.database import async_session_maker
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags = ["Авторизация и аутентификация"])
auth = AuthService()

@router.post("/register")
async def register_user(data: UserRequestAdd):
    
    hashed_password = auth.get_password_hash(data.password)
    
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestAdd, response : Response):
    
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с такой почтой не зарегистрирован")

        if not auth.verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        access_token = auth.create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}



@router.get("/me")
async def get_me(user_id: UserIdDep):

    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user
    


@router.post("/logout")
async def logout(response : Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}