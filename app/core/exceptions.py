from fastapi import HTTPException

class VMNotFoundException(HTTPException):
    def __init__(self, vm_id: str):
        super().__init__(status_code=404, detail=f"VM '{vm_id}' not found")

class VMOperationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)

class OpenStackConnectionException(HTTPException):
    def __init__(self):
        super().__init__(status_code=503, detail="OpenStack service unavailable")