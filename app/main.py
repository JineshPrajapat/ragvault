from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.startup import init_database, init_redis, shutdown_redis
from app.middleware.app_token import AppTokenDependency
from app.modules.auth.middleware import AuthDependency
from app.handlers.exception_handlers import http_exception_handler
from app.api.v1 import api_v1_router

app = FastAPI(
    title="RAGVault", 
    version="0.1.0",
    dependencies=[
        Depends(AppTokenDependency()),
        Depends(AuthDependency())
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mxicoders.co", "http://mxicoders.co", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_exception_handler)

app.mount(
    "/static",
    StaticFiles(directory="./uploads"),
    name="static"
)

@app.on_event("startup")
async def startup():
    await init_database()
    await init_redis()


@app.on_event("shutdown")
async def shutdown():
    await shutdown_redis()

app.include_router(api_v1_router, prefix="/api/v1")