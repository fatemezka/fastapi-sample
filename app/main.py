from fastapi import FastAPI
from app.db.base import create_all_tables
import logging
from app.utils.error_handler import CustomException
from fastapi.responses import JSONResponse
from app.middleware import CustomMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.test.test_route import router as test_router
from app.api.v1.token.token_route import router as token_router
from app.api.v1.user.user_route import router as user_router
# from app.api.v1.lawyer.lawyer_route import router as lawyer_router
# from app.api.v1.request.request_route import router as request_router
# from app.api.v1.question.question_route import router as question_router


app = FastAPI(
    title="GoodLawyer",
    description="This is a Goodlawyer project which is written and developed by FastAPI."
)

# Logging
logging.basicConfig(filename='errors.log', level=logging.ERROR)


@app.on_event("startup")
async def startup_db():
    await create_all_tables()


# Middlewares
allowed_origins = [
    "http://localhost:3000",  # TODO get from redis
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CustomMiddleware)

# Routes
ROUTE_PREFIX = ""  # TODO "/api/v1"
app.include_router(test_router, prefix=ROUTE_PREFIX + "/test", tags=["Test"])
app.include_router(token_router, prefix=ROUTE_PREFIX +
                   "/token", tags=["Token"])
app.include_router(user_router, prefix=ROUTE_PREFIX + "/user", tags=["User"])
# app.include_router(lawyer_router, prefix=ROUTE_PREFIX + "/lawyer", tags=["Lawyer"])
# app.include_router(request_router, prefix=ROUTE_PREFIX + "/request", tags=["Request"])
# app.include_router(question_router, prefix=ROUTE_PREFIX + "/question", tags=["Question"])
