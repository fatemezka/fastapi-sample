import os
from jose import JWTError, jwt


def token_parser(request):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    token = request.headers[os.getenv("AUTH_HEADER_NAME")].split()[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except:
        print("Token parser error--------------------------")
        return JWTError

    return user_id
