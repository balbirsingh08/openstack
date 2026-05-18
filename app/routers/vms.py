from fastapi import APIRouter, status
from app.schemas.vm import (
    VMCreateRequest, VMActionRequest,
    VMResponse, VMListResponse, MessageResponse
)
from app.services.openstack import vm_service

router = APIRouter(prefix="/api/v1/vms", tags=["VMs"])

@router.post("/", response_model=VMResponse, status_code=status.HTTP_201_CREATED,
             summary="Create a new VM")
def create_vm(request: VMCreateRequest):
    """Provision a new virtual machine on OpenStack."""
    vm = vm_service.create_vm(
        name=request.name, flavor=request.flavor, image=request.image,
        network=request.network, key_pair=request.key_pair,
        security_groups=request.security_groups, metadata=request.metadata
    )
    return vm.__dict__

@router.get("/", response_model=VMListResponse, summary="List all VMs")
def list_vms():
    """Return all active virtual machines."""
    vms = vm_service.list_vms()
    return {"total": len(vms), "vms": [v.__dict__ for v in vms]}

@router.get("/{vm_id}", response_model=VMResponse, summary="Get VM details")
def get_vm(vm_id: str):
    """Fetch details of a specific VM by ID."""
    vm = vm_service.get_vm(vm_id)
    return vm.__dict__

@router.post("/{vm_id}/action", response_model=VMResponse, summary="Perform VM action")
def vm_action(vm_id: str, request: VMActionRequest):
    """Perform lifecycle action: start | stop | reboot | pause."""
    vm = vm_service.perform_action(vm_id, request.action)
    return vm.__dict__

@router.delete("/{vm_id}", response_model=MessageResponse, summary="Delete a VM")
def delete_vm(vm_id: str):
    """Terminate and remove a VM permanently."""
    vm_service.delete_vm(vm_id)
    return {"message": f"VM '{vm_id}' deleted successfully.", "vm_id": vm_id}