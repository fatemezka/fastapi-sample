import os
from datetime import datetime
from fastapi import status, HTTPException
import logging


class CustomException(HTTPException):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.detail = message


class ErrorHandler:
    @staticmethod
    def not_found(item: str):
        raise CustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{item} Not Found"
        )

    @staticmethod
    def user_unauthorized():
        header_name = os.getenv("AUTH_HEADER_NAME")
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=f"Could not validate user credentials ({header_name} header)"
        )

    @staticmethod
    def lawyer_unauthorized():
        header_name = os.getenv("AUTH_HEADER_NAME")
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=f"Could not validate lawyer credentials ({header_name} Header)"
        )

    @staticmethod
    def access_denied(item: str):
        raise CustomException(
            status_code=status.HTTP_403_FORBIDDEN,
            message=f"You do not have access to this {item}"
        )

    @staticmethod
    def bad_request(custom_message):
        header_name = os.getenv("AUTH_HEADER_NAME")
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=custom_message
        )

    @staticmethod
    def internal_server_error(error):
        logging.error(f"An error occurred at {datetime.now()}: {error}")
        print(error)  # todo remove
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal Server Error"
        )

    @staticmethod
    def database_error(error):
        logging.error(
            f"An SQLAlchemy error occurred at {datetime.now()}: {error}")
        print(error)  # todo remove
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Something went wrong in database, so all operations rolled back"
        )
