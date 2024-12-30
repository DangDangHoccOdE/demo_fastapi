import os
from fastapi import FastAPI
import logging
import logging.config

from api.v1.api_v1 import api_router
from middlewares.cors_middleware import add_cors_middleware
from middlewares.logging_middleware import LoggingMiddleware
from core.config import settings
from app.helpers.exception_handler import CustomException, global_exception_handler, custom_exception_handler

log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers = False)

app = FastAPI(
    title = settings.PROJECT_NAME,
    description = "This is a sample project to demonstrate FastAPI structure",
    version = "1.0.0",
)

# Gắn router từ api_v1
app.include_router(api_router)

# Register middleware
add_cors_middleware(app)
app.add_middleware(LoggingMiddleware)

# Register exception handler
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Sample Project"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)