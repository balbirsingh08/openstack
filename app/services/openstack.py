import uuid
from datetime import datetime
from typing import List, Optional, Dict
from app.models.vm import VM, VMStatus
from app.core.config import settings
from app.core.exceptions import VMNotFoundException, VMOperationException, OpenStackConnectionException
import logging

logger = logging.getLogger(__name__)

# ── In-memory store for mock mode ───────────────────────────
_mock_store: Dict[str, VM] = {}

class VMService:
    def __init__(self):
        self.use_mock = settings.use_mock
        if not self.use_mock:
            self._init_openstack()

    def _init_openstack(self):
        """Initialize real OpenStack connection via openstacksdk."""
        try:
            import openstack
            self.conn = openstack.connect(
                auth_url=settings.os_auth_url,
                project_name=settings.os_project_name,
                username=settings.os_username,
                password=settings.os_password,
                user_domain_name=settings.os_user_domain_name,
                project_domain_name=settings.os_project_domain_name,
            )
            logger.info("Connected to OpenStack successfully.")
        except Exception as e:
            logger.error(f"OpenStack connection failed: {e}")
            raise OpenStackConnectionException()

    # ── CREATE ───────────────────────────────────────────────
    def create_vm(self, name: str, flavor: str, image: str,
                  network: str = "default", key_pair: Optional[str] = None,
                  security_groups: List[str] = ["default"],
                  metadata: Dict = {}) -> VM:
        if self.use_mock:
            vm_id = str(uuid.uuid4())
            vm = VM(id=vm_id, name=name, flavor=flavor, image=image,
                    status=VMStatus.BUILD, ip_address=f"192.168.1.{len(_mock_store)+10}",
                    created_at=datetime.utcnow(), metadata=metadata)
            _mock_store[vm_id] = vm
            # Simulate going ACTIVE after creation
            vm.status = VMStatus.ACTIVE
            logger.info(f"[MOCK] Created VM: {vm_id}")
            return vm
        else:
            server = self.conn.compute.create_server(
                name=name,
                flavor_id=self._get_flavor_id(flavor),
                image_id=self._get_image_id(image),
                networks=[{"uuid": self._get_network_id(network)}],
                key_name=key_pair,
                security_groups=[{"name": sg} for sg in security_groups],
                metadata=metadata,
            )
            self.conn.compute.wait_for_server(server)
            return self._server_to_vm(server)

    # ── LIST ─────────────────────────────────────────────────
    def list_vms(self) -> List[VM]:
        if self.use_mock:
            return [v for v in _mock_store.values() if v.status != VMStatus.DELETED]
        else:
            servers = self.conn.compute.servers()
            return [self._server_to_vm(s) for s in servers]

    # ── GET ──────────────────────────────────────────────────
    def get_vm(self, vm_id: str) -> VM:
        if self.use_mock:
            vm = _mock_store.get(vm_id)
            if not vm or vm.status == VMStatus.DELETED:
                raise VMNotFoundException(vm_id)
            return vm
        else:
            server = self.conn.compute.find_server(vm_id)
            if not server:
                raise VMNotFoundException(vm_id)
            return self._server_to_vm(server)

    # ── ACTION (start/stop/reboot/pause) ─────────────────────
    def perform_action(self, vm_id: str, action: str) -> VM:
        vm = self.get_vm(vm_id)
        action = action.lower()

        if self.use_mock:
            if action == "start":
                if vm.status not in [VMStatus.STOPPED, VMStatus.PAUSED]:
                    raise VMOperationException(f"Cannot start a VM in '{vm.status}' state")
                vm.status = VMStatus.ACTIVE
            elif action == "stop":
                if vm.status != VMStatus.ACTIVE:
                    raise VMOperationException(f"Cannot stop a VM in '{vm.status}' state")
                vm.status = VMStatus.STOPPED
            elif action == "reboot":
                if vm.status != VMStatus.ACTIVE:
                    raise VMOperationException(f"Cannot reboot a VM in '{vm.status}' state")
                vm.status = VMStatus.REBOOT
                vm.status = VMStatus.ACTIVE  # Back to active after reboot
            elif action == "pause":
                if vm.status != VMStatus.ACTIVE:
                    raise VMOperationException(f"Cannot pause a VM in '{vm.status}' state")
                vm.status = VMStatus.PAUSED
            else:
                raise VMOperationException(f"Unknown action '{action}'. Allowed: start, stop, reboot, pause")
            logger.info(f"[MOCK] Action '{action}' on VM {vm_id}")
            return vm
        else:
            server = self.conn.compute.find_server(vm_id)
            if action == "start":
                self.conn.compute.start_server(server)
            elif action == "stop":
                self.conn.compute.stop_server(server)
            elif action == "reboot":
                self.conn.compute.reboot_server(server, reboot_type="SOFT")
            elif action == "pause":
                self.conn.compute.pause_server(server)
            else:
                raise VMOperationException(f"Unknown action: {action}")
            return self._server_to_vm(self.conn.compute.get_server(vm_id))

    # ── DELETE ───────────────────────────────────────────────
    def delete_vm(self, vm_id: str) -> bool:
        vm = self.get_vm(vm_id)
        if self.use_mock:
            vm.status = VMStatus.DELETED
            logger.info(f"[MOCK] Deleted VM: {vm_id}")
            return True
        else:
            server = self.conn.compute.find_server(vm_id)
            self.conn.compute.delete_server(server)
            self.conn.compute.wait_for_delete(server)
            return True

    # ── Helpers (real OpenStack) ─────────────────────────────
    def _server_to_vm(self, server) -> VM:
        addresses = server.addresses
        ip = None
        for net_addresses in addresses.values():
            for addr in net_addresses:
                ip = addr.get("addr")
                break
        return VM(id=server.id, name=server.name,
                  flavor=server.flavor.get("original_name", "unknown"),
                  image=server.image.get("id", "unknown"),
                  status=VMStatus(server.status),
                  ip_address=ip,
                  created_at=datetime.fromisoformat(server.created_at))

    def _get_flavor_id(self, name: str) -> str:
        flavor = self.conn.compute.find_flavor(name)
        if not flavor:
            raise VMOperationException(f"Flavor '{name}' not found")
        return flavor.id

    def _get_image_id(self, name: str) -> str:
        image = self.conn.image.find_image(name)
        if not image:
            raise VMOperationException(f"Image '{name}' not found")
        return image.id

    def _get_network_id(self, name: str) -> str:
        network = self.conn.network.find_network(name)
        if not network:
            raise VMOperationException(f"Network '{name}' not found")
        return network.id

# Singleton instance
vm_service = VMService()