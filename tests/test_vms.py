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
    return data["id"]

def test_list_vms(client):
    r = client.get("/api/v1/vms/")
    assert r.status_code == 200
    assert "vms" in r.json()

def test_vm_lifecycle(client):
    # Create
    r = client.post("/api/v1/vms/", json={"name": "lifecycle-vm", "flavor": "m1.small", "image": "ubuntu-22.04"})
    vm_id = r.json()["id"]

    # Stop
    r = client.post(f"/api/v1/vms/{vm_id}/action", json={"action": "stop"})
    assert r.json()["status"] == "STOPPED"

    # Start
    r = client.post(f"/api/v1/vms/{vm_id}/action", json={"action": "start"})
    assert r.json()["status"] == "ACTIVE"

    # Delete
    r = client.delete(f"/api/v1/vms/{vm_id}")
    assert r.status_code == 200

def test_vm_not_found(client):
    r = client.get("/api/v1/vms/nonexistent-id")
    assert r.status_code == 404