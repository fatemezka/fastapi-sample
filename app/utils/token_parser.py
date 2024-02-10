import os
from jose import JWTError, jwt


def token_parser(request):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    AUTH_HEADER_NAME = os.getenv("AUTH_HEADER_NAME")
    token = request.headers[AUTH_HEADER_NAME].split()[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except:
        return JWTError

    return user_id
