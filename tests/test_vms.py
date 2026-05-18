import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_create_vm(client):
    payload = {"name": "test-vm", "flavor": "m1.small", "image": "ubuntu-22.04"}
    r = client.post("/api/v1/vms/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "test-vm"
    assert data["status"] == "ACTIVE"


def test_list_vms(client):
    r = client.get("/api/v1/vms/")
    assert r.status_code == 200
    assert "vms" in r.json()


def test_get_vm(client):
    r = client.post("/api/v1/vms/", json={"name": "get-vm", "flavor": "m1.small", "image": "ubuntu-22.04"})
    vm_id = r.json()["id"]
    r = client.get(f"/api/v1/vms/{vm_id}")
    assert r.status_code == 200
    assert r.json()["id"] == vm_id


def test_vm_lifecycle(client):
    r = client.post("/api/v1/vms/", json={"name": "lifecycle-vm", "flavor": "m1.small", "image": "ubuntu-22.04"})
    vm_id = r.json()["id"]

    r = client.post(f"/api/v1/vms/{vm_id}/action", json={"action": "stop"})
    assert r.json()["status"] == "STOPPED"

    r = client.post(f"/api/v1/vms/{vm_id}/action", json={"action": "start"})
    assert r.json()["status"] == "ACTIVE"

    r = client.delete(f"/api/v1/vms/{vm_id}")
    assert r.status_code == 200


def test_reboot_vm(client):
    r = client.post("/api/v1/vms/", json={"name": "reboot-vm", "flavor": "m1.small", "image": "ubuntu-22.04"})
    vm_id = r.json()["id"]
    r = client.post(f"/api/v1/vms/{vm_id}/action", json={"action": "reboot"})
    assert r.json()["status"] == "ACTIVE"


def test_pause_and_start(client):
    r = client.post("/api/v1/vms/", json={"name": "pause-vm", "flavor": "m1.small", "image": "ubuntu-22.04"})
    vm_id = r.json()["id"]

    r = client.post(f"/api/v1/vms/{vm_id}/action", json={"action": "pause"})
    assert r.json()["status"] == "PAUSED"

    r = client.post(f"/api/v1/vms/{vm_id}/action", json={"action": "start"})
    assert r.json()["status"] == "ACTIVE"


def test_invalid_action(client):
    r = client.post("/api/v1/vms/", json={"name": "action-vm", "flavor": "m1.small", "image": "ubuntu-22.04"})
    vm_id = r.json()["id"]
    r = client.post(f"/api/v1/vms/{vm_id}/action", json={"action": "fly"})
    assert r.status_code == 400


def test_stop_already_stopped(client):
    r = client.post("/api/v1/vms/", json={"name": "stop-vm", "flavor": "m1.small", "image": "ubuntu-22.04"})
    vm_id = r.json()["id"]
    client.post(f"/api/v1/vms/{vm_id}/action", json={"action": "stop"})
    r = client.post(f"/api/v1/vms/{vm_id}/action", json={"action": "stop"})
    assert r.status_code == 400


def test_vm_not_found(client):
    r = client.get("/api/v1/vms/nonexistent-id")
    assert r.status_code == 404


def test_delete_nonexistent(client):
    r = client.delete("/api/v1/vms/fake-id-999")
    assert r.status_code == 404