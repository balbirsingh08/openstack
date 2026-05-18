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