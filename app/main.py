from fastapi import FastAPI, Path, Query
from .database import create_tables, SessionLocal
from .routes.user import router as user_router

app = FastAPI()

@app.on_event("startup")
async def startup_db():
    # initial database (on startup)
    create_tables()


# routes
app.include_router(user_router, prefix="/user", tags=["user"])
