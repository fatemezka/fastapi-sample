class CustomException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class ErrorHandler:
    @staticmethod
    def not_found(item: str):
        raise CustomException(status_code=404, detail=f"{item} Not Found")

    @staticmethod
    def internal_server_error():
        raise CustomException(
            status_code=500, detail="Internal Server Error")
