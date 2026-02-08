from fastapi import HTTPException
import jwt
from pwdlib import PasswordHash
from datetime import timezone, timedelta,datetime
from src.config import settings


class AuthService:
    password_hash = PasswordHash.recommended()

    def get_password_hash(self,password):
        return self.password_hash.hash(password)

    def create_access_token(self,data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= ({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt


    def verify_password(self,plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)
    
    def decode_token(self,token : str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM,verify=True)
        except:
            raise HTTPException(status_code=401, detail="Токен истек или невалиден")
        
    
