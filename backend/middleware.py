from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import traceback
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger()
        logger.info(f"Request: {request.method} {request.url}")
        print(f"Request: {request.method} {request.url}")
        try:
            response = await call_next(request)
            logger.info(f"Response: {response.status_code} {request.method} {request.url}")
            print(f"Response: {response.status_code} {request.method} {request.url}")
            return response
        except Exception as exc:
            logger.error(f"Exception: {exc}\n{traceback.format_exc()}")
            print(f"Exception: {exc}\n{traceback.format_exc()}")
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# Add detailed request/response logging middleware
class DetailedRequestResponseLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        idem = f"{time.time()}-{request.method}-{request.url}"
        logging.info(f"[REQUEST] {idem} path={request.url.path} query={request.url.query} headers={dict(request.headers)}")
        print(f"[REQUEST] {idem} path={request.url.path} query={request.url.query} headers={dict(request.headers)}")
        body = await request.body()
        logging.info(f"[REQUEST BODY] {idem} body={body.decode(errors='replace')}")
        print(f"[REQUEST BODY] {idem} body={body.decode(errors='replace')}")
        response = await call_next(request)
        logging.info(f"[RESPONSE] {idem} status={response.status_code}")
        print(f"[RESPONSE] {idem} status={response.status_code}")
        return response

def add_middlewares(app):
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(DetailedRequestResponseLogger)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 