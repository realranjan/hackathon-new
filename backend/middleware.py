from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import traceback

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger()
        logger.info(f"Request: {request.method} {request.url}")
        try:
            response = await call_next(request)
            logger.info(f"Response: {response.status_code} {request.method} {request.url}")
            return response
        except Exception as exc:
            logger.error(f"Exception: {exc}\n{traceback.format_exc()}")
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

def add_middlewares(app):
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 