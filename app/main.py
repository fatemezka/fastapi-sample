from fastapi import FastAPI, Request
from app.database import create_tables, SessionLocal
from starlette.middleware.base import BaseHTTPMiddleware
from app.middleware import request_handler
from app.routes.user import router as user_router


app = FastAPI()


@app.on_event("startup")
async def startup_db():
    # initial database (on startup)
    create_tables()

# middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=request_handler)

# routes
app.include_router(user_router, prefix="/user", tags=["user"])
