from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vms
from app.core.config import settings
import logging

logging.basicConfig(level=settings.log_level)

app = FastAPI(
    title="OpenStack VM Lifecycle API",
    description="REST API for managing OpenStack VM lifecycle operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vms.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "mode": "mock" if settings.use_mock else "openstack"}