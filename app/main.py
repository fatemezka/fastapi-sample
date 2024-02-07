from fastapi import FastAPI, Path, Query
from .database import create_tables

from .routes.user import router as user_router

app = FastAPI()

create_tables()

# routes
app.include_router(user_router, prefix="/user", tags=["user"])
