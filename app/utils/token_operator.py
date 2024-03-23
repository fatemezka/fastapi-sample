import os
from jose import jwt
from datetime import datetime, timedelta, timezone


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"created_at": str(datetime.now())})
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
