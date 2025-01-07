import os
from fastapi import APIRouter, Depends, HTTPException, Response
from google.oauth2 import id_token
import logging
from google.auth.transport import requests as google_requests
from pydantic import BaseModel
from infrastructure.repositories.user_repository import UserRepository
from domain.entities.entities import User as UserEntity
from interfaces.service.jwt_service import generate_jwt


router = APIRouter()
# 获取 logger
logger = logging.getLogger(__name__)


# 替换为您的 Google Client ID
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

class GoogleLoginRequest(BaseModel):
    token: str

class User(BaseModel):
    id: str
    email: str
    name: str
    picture: str

@router.post("/auth/google-login")
async def google_login(
    request: GoogleLoginRequest,
    response: Response,
    user_repo: UserRepository = Depends(UserRepository)
):
    # 添加响应头
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
    
    try:
        idinfo = id_token.verify_oauth2_token(request.token, google_requests.Request(), GOOGLE_CLIENT_ID)
        google_id = idinfo['sub']
        email = idinfo.get('email')
        name = idinfo.get('name')
        picture = idinfo.get('picture')

        # 检查用户是否存在
        user = user_repo.get_user_by_google_id(google_id)

        if user:
            # 更新现有用户信息
            user = user_repo.update_user(
                google_id,
                email=email,
                username=name,
                profile_picture=picture
            )
        else:
            # 创建新用户
            user = user_repo.create_user(
                google_id=google_id,
                email=email,
                username=name,
                profile_picture=picture
            )

        # 创建用户对象用于生成 JWT
        user_entity = User(
            id=user['google_id'],
            email=user['email'],
            name=user['username'],
            picture=user['profile_picture']
        )
        
        # 生成 JWT
        token = generate_jwt(user_entity.dict())

        return {
            'message': '登录成功',
            'token': token,
            'user': user_entity.dict()
        }
    except ValueError as e:
        logger.error(f"Google token verification failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid Google token or user operation failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Login process error: {str(e)}", exc_info=True)
        logger.error("Full error details:", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error during login process: {str(e)}"
        )