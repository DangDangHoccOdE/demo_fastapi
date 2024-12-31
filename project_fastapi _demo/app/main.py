import os
from fastapi import FastAPI
import logging.config
from app.api.v1.api_v1 import api_router
from app.core.config import get_settings
from app.middlewares.cors_middleware import add_cors_middleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.helpers.exception_handler import CustomException, global_exception_handler, custom_exception_handler

log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers = False)
settings = get_settings()

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