from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from scheduler import start_scheduler
from auth import auth_router
from routes.shipment import shipment_router
from routes.disruption import disruption_router
from routes.health import health_router
from logging_config import setup_logging
from middleware import add_middlewares

limiter = Limiter(key_func=get_remote_address, default_limits=["100/hour"])
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

setup_logging()
add_middlewares(app)

app.include_router(auth_router)
app.include_router(shipment_router)
app.include_router(disruption_router)
app.include_router(health_router)

start_scheduler() 