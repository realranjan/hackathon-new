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
from routes.admin import admin_router
from logging_config import setup_logging
from middleware import add_middlewares
from fastapi.openapi.utils import get_openapi

limiter = Limiter(key_func=get_remote_address, default_limits=["100/hour"])
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_logging()
add_middlewares(app)

app.include_router(auth_router)
app.include_router(shipment_router)
app.include_router(disruption_router)
app.include_router(health_router)
app.include_router(admin_router)

start_scheduler()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SupplyWhiz API",
        version="1.0.0",
        description="Multi-Agent Supply Chain Analysis Platform API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for op in path.values():
            if "security" not in op:
                op["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi 