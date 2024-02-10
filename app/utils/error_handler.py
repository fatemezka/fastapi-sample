import os
from datetime import datetime
from fastapi import status
import logging


class CustomException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.detail = {
            "status_code": status_code,
            "error_message": message
        }


class ErrorHandler:
    @staticmethod
    def not_found(item: str, error):
        logging.error(f"An error occurred at {datetime.now()}: {error}")
        raise CustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{item} Not Found"
        )

    @staticmethod
    def unauthorized(error):
        logging.error(f"An error occurred at {datetime.now()}: {error}")
        header_name = os.getenv("AUTH_HEADER_NAME")
        raise CustomException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=f"Could Not Validate Credentials ({header_name} Header)"
        )

    @staticmethod
    def bad_request(custom_message, error):
        logging.error(f"An error occurred at {datetime.now()}: {error}")
        header_name = os.getenv("AUTH_HEADER_NAME")
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=custom_message
        )

    @staticmethod
    def internal_server_error(error):
        logging.error(f"An error occurred at {datetime.now()}: {error}")
        raise CustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal Server Error"
        )
