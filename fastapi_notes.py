from enum import Enum
from fastapi import APIRouter, Depends, Query
from typing import Annotated, Union
from typing import List

router = APIRouter()


# optional q
q: str | None = None
q: str | None = Query(default=None)
q: Annotated[str | None, Query(max_length=10)] = None
q: Union[str, None] = Query(default=None, max_length=50)
q: Annotated[str | None, Query(min_length=3, max_length=50)] = "fateme"
q: Annotated[ str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None


# required q
q: str => value is required
q: Annotated[str, Query(min_length=3)] = ...   => value is required


# list q
q: Annotated[List[str], Query()] = []    # http://localhost:8000/items/?q=foo&q=bar  > q = [foo, bar]


# describe the query
q: Annotated[
        str | None,
        Query(
            title="Query string",
            alias="item-query",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True, # show it is deprecated
            include_in_schema=False # make it hidden in doc
        ),
    ] = None,












@router.get("/users/")
async def read_users(q: Annotated[str | None, Query(max_length=10)] = None):
    return q


@router.get("/items/{item_id}")
async def read_item(item_id: int, q1: str | None = "Fateme"):
    return {"item_id": item_id, "name": q1}


@router.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
