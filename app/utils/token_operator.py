import os
from datetime import datetime
from jose import JWTError, jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
AUTH_HEADER_NAME = os.getenv("AUTH_HEADER_NAME")


def token_parser(request):
    token = request.headers[AUTH_HEADER_NAME].split()[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except:
        return JWTError

    return user_id


def token_generator(user_id, is_lawyer):
    to_encode_data = {
        "user_id": user_id,
        "is_lawyer": is_lawyer,
        "created_at": str(datetime.now())
    }
    return jwt.encode(to_encode_data, SECRET_KEY, ALGORITHM)
