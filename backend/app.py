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
import logging
from slowapi.extension import Limiter as SlowAPILimiter
from fastapi import Depends
from routes.integrations import integrations_router
from routes.analytics import analytics_router

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute", "100/hour"])
app = FastAPI()
print("[APP] FastAPI app instance created.")
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
print("[APP] Logging configured.")
add_middlewares(app)
print("[APP] Custom middlewares added.")

app.include_router(auth_router)
print("[APP] Auth router included.")
app.include_router(shipment_router)
print("[APP] Shipment router included.")
app.include_router(disruption_router)
print("[APP] Disruption router included.")
app.include_router(health_router)
print("[APP] Health router included.")
app.include_router(admin_router)
print("[APP] Admin router included.")
app.include_router(integrations_router)
print("[APP] Integrations router included.")
app.include_router(analytics_router)
print("[APP] Analytics router included.")

start_scheduler()
print("[APP] Scheduler started.")

def custom_openapi():
    print("[APP] Generating custom OpenAPI schema.")
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

# Example: Add per-endpoint rate limiting
@health_router.get("/limited_healthz")
@limiter.limit("5/minute")
async def limited_healthz(request):
    print("[API] /limited_healthz endpoint called (rate limited)")
    return {"status": "ok (rate limited)"} 