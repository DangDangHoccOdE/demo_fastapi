import logging
from fastapi import Request
from starlette.responses import JSONResponse

logger = logging.getLogger()

class CustomException(Exception):
    http_code: int
    message: str

    def __init__(self, http_code: int = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.message = message

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.http_code,
        content = {'message': exc.message}
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info = True)

    return JSONResponse(
        status_code = 500,
        content= {"message":"Internal server error."}
    )