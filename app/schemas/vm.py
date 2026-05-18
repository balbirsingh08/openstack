from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from app.models.vm import VMStatus

# ── Request Schemas ──────────────────────────────────────────
class VMCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="my-web-server")
    flavor: str = Field(..., example="m1.small")   # e.g. m1.small, m1.medium
    image: str = Field(..., example="ubuntu-22.04")
    network: Optional[str] = Field(default="default", example="default")
    key_pair: Optional[str] = Field(default=None, example="my-keypair")
    security_groups: Optional[List[str]] = Field(default=["default"])
    metadata: Optional[Dict[str, str]] = Field(default={})

class VMActionRequest(BaseModel):
    action: str = Field(..., example="start")  # start, stop, reboot, pause

# ── Response Schemas ─────────────────────────────────────────
class VMResponse(BaseModel):
    id: str
    name: str
    flavor: str
    image: str
    status: VMStatus
    ip_address: Optional[str] = None
    created_at: datetime
    metadata: Dict = {}

    class Config:
        from_attributes = True

class VMListResponse(BaseModel):
    total: int
    vms: List[VMResponse]

class MessageResponse(BaseModel):
    message: str
    vm_id: Optional[str] = None