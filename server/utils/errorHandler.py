from .response import APIResponse
from functools import wraps

class ApiError(APIResponse):
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