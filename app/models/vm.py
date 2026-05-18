from enum import Enum
from datetime import datetime
from typing import Optional, Dict

class VMStatus(str, Enum):
    ACTIVE = "ACTIVE"
    STOPPED = "STOPPED"
    PAUSED = "PAUSED"
    DELETED = "DELETED"
    BUILD = "BUILD"
    ERROR = "ERROR"
    REBOOT = "REBOOT"

class VM:
    def __init__(self, id: str, name: str, flavor: str, image: str,
                 status: VMStatus, ip_address: Optional[str] = None,
                 created_at: Optional[datetime] = None,
                 metadata: Optional[Dict] = None):
        self.id = id
        self.name = name
        self.flavor = flavor
        self.image = image
        self.status = status
        self.ip_address = ip_address
        self.created_at = created_at or datetime.utcnow()
        self.metadata = metadata or {}