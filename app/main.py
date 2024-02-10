from fastapi import FastAPI, Request
from app.database import create_tables
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.error_handler import CustomException
from fastapi.responses import JSONResponse
from app.middleware import CustomMiddleware
from app.routes.user import router as user_router
from app.routes.lawyer import router as lawyer_router


app = FastAPI()

# logging
logging.basicConfig(filename='errors.log', level=logging.ERROR)


# create tables on startup
@app.on_event("startup")
async def startup_db():
    # initial database (on startup)
    create_tables()


# custom error handler
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "message": exc.detail
        }
    )


# middleware
app.add_middleware(CustomMiddleware)


# routes
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(lawyer_router, prefix="/lawyer", tags=["lawyer"])
