# app/main.py

from fastapi import FastAPI
from framework.middleware.logging_middleware import LoggingMiddleware
from app.routers.user_info import router as user_info_router

app = FastAPI()

app.add_middleware(LoggingMiddleware)

app.include_router(user_info_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
