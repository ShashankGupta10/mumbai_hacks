import json
from flask import Response
from functools import wraps

class ApiResponse:
    def __init__(self, status: int, data: dict | None, success: bool = True, message: str = "success"):
        self.response = {}
        self.response["status"] = status
        self.response["body"] = data
        self.response["message"] = message
        self.response["success"] = success
        self.json = Response(
            response=json.dumps(self.response),
            mimetype="application/json",
            status=self.response["status"]
        )


class ApiError(ApiResponse):
    def __init__(self, status: int, message: str):
        super().__init__(status, None, message=message, success=False)


def handle(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return ApiError(200, e.__doc__).json
    return wrapped