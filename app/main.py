from fastapi import FastAPI, Request
from app.database import create_tables
import logging
from app.utils.error_handler import CustomException
from fastapi.responses import JSONResponse
from app.middleware import CustomMiddleware
from app.api.v1.user.user_route import router as user_router
from app.api.v1.lawyer.lawyer_route import router as lawyer_router
from app.api.v1.request.request_route import router as request_router
from app.api.v1.question.question_route import router as question_router


app = FastAPI()

# Logging
logging.basicConfig(filename='errors.log', level=logging.ERROR)


# Create all tables
@app.on_event("startup")
async def startup_db():
    # initial database (on startup)
    create_tables()


# Error handler
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "message": exc.detail
        }
    )


# Middleware
app.add_middleware(CustomMiddleware)


# Routes
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(lawyer_router, prefix="/lawyer", tags=["Lawyer"])
app.include_router(request_router, prefix="/request", tags=["Request"])
app.include_router(question_router, prefix="/question", tags=["Question"])
