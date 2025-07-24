import os
import requests
from fastapi import APIRouter, Request

health_router = APIRouter()

@health_router.get("/")
async def root(request: Request):
    print("[API] / (root) health endpoint called")
    return {"message": "Welcome to SupplyWhiz API"}

@health_router.get("/healthz")
async def healthz():
    print("[API] /healthz endpoint called")
    return {"status": "ok"} 