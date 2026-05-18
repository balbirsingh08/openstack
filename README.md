# OpenStack VM Lifecycle Management API

REST API built with **FastAPI + Python** to manage OpenStack VM lifecycle operations.

## Architecture
- **FastAPI** — async REST framework
- **openstacksdk** — OpenStack integration
- **Mock Mode** — works without real OpenStack (USE_MOCK=true)
- **Pydantic v2** — request/response validation
- **Docker** — containerized deployment

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| POST | /api/v1/vms/ | Create VM |
| GET | /api/v1/vms/ | List all VMs |
| GET | /api/v1/vms/{id} | Get VM details |
| POST | /api/v1/vms/{id}/action | Start/Stop/Reboot/Pause |
| DELETE | /api/v1/vms/{id} | Delete VM |

## Quick Start

```bash
git clone <repo>
cd openstack-vm-api
cp .env.example .env
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open: http://localhost:8000/docs

## Running Tests
```bash
pytest tests/ -v --cov=app
```

## Design Decisions
- **Mock mode** allows dev/testing without real OpenStack
- **Service layer** separates business logic from routing
- **Pydantic schemas** give strict validation + auto docs
- **Enum-based VM states** enforce valid state transitions

## Roadmap
- [ ] JWT Authentication
- [ ] Redis caching for VM state
- [ ] Async operations with Celery
- [ ] Prometheus metrics endpoint
- [ ] Multi-tenant support
- [ ] WebSocket for real-time VM status

list vm
<img width="1269" height="653" alt="image" src="https://github.com/user-attachments/assets/33815250-3194-4f62-9046-85844dff3359" />

created vm
<img width="1018" height="584" alt="image" src="https://github.com/user-attachments/assets/8b808d72-c5c5-40fb-b121-161dde0595e7" />

deleted vm
<img width="1157" height="595" alt="image" src="https://github.com/user-attachments/assets/996f3de7-ec6b-4b2a-a5b4-8c273aa238b3" />
