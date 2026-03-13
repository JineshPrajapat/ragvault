from fastapi import APIRouter
from .auth import router as auth_router
from .user import router as user_router
from .chat_session import router as chat_session_router

api_v1_router = APIRouter()

routers = [
    (auth_router, "/auth"),
    (user_router, "/user"),
    (chat_session_router, "/sessions")
]

for router, prefix in routers:
    api_v1_router.include_router(router, prefix=prefix)
