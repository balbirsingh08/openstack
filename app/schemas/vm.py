from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from app.models.vm import VMStatus


class VMCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    flavor: str
    image: str
    network: Optional[str] = "default"
    key_pair: Optional[str] = None
    security_groups: Optional[List[str]] = ["default"]
    metadata: Optional[Dict[str, str]] = {}

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "my-web-server",
                "flavor": "m1.small",
                "image": "ubuntu-22.04",
                "network": "default",
                "security_groups": ["default"],
                "metadata": {"env": "dev"}
            }
        }
    }


class VMActionRequest(BaseModel):
    action: str

    model_config = {
        "json_schema_extra": {"example": {"action": "stop"}}
    }


class VMResponse(BaseModel):
    id: str
    name: str
    flavor: str
    image: str
    status: VMStatus
    ip_address: Optional[str] = None
    created_at: datetime
    metadata: Dict = {}

    model_config = {"from_attributes": True} 


class VMListResponse(BaseModel):
    total: int
    vms: List[VMResponse]


class MessageResponse(BaseModel):
    message: str
    vm_id: Optional[str] = None