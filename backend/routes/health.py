from fastapi import APIRouter, Request

health_router = APIRouter()

@health_router.get("/")
async def root(request: Request):
    return {"message": "Welcome to SupplyWhiz API"}

@health_router.get("/healthz")
async def healthz():
    return {"status": "ok"} 