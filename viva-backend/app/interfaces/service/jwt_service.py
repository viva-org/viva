import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
from typing import Dict

# 这个密钥应该保密，并且最好从环境变量中读取
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 令牌有效期，可以根据需要调整

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_jwt(user: Dict) -> str:
    data = user.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, JWT_SECRET, algorithm=ALGORITHM) # type: ignore
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM]) # type: ignore
        user_id: str = payload.get("id")
        print("user_id", user_id)
        if user_id is None:
            raise credentials_exception
        return {"id": user_id}
    except jwt.PyJWTError:
        raise credentials_exception