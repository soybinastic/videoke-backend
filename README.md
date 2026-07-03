# Videoke Backend

Online party karaoke API — Django REST Framework + Django Channels.

## Architecture

Layered design following SOLID principles:

```
rooms/
├── domain/           # Constants, domain exceptions
├── parsers/          # Strategy: VideoUrlParser → YouTubeUrlParser
├── repositories/     # Data access (Repository pattern)
├── services/         # Business logic (SRP per service)
│   ├── room_service.py
│   ├── queue_service.py
│   └── reaction_service.py
├── serializers/      # DTOs / API contracts
├── api/              # Thin controllers (APIView)
│   └── views/
├── consumers/        # WebSocket + message dispatcher
└── container.py      # Dependency injection factory
```

| Principle | Application |
|-----------|-------------|
| **S**ingle Responsibility | Each service owns one domain concern |
| **O**pen/Closed | New video parsers or WS handlers without changing core logic |
| **L**iskov | `VideoUrlParser` implementations are interchangeable |
| **I**nterface Segregation | `RoomEventBroadcaster` protocol for real-time events |
| **D**ependency Inversion | Services depend on abstractions, wired via `container.py` |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

## Run

```bash
source .venv/bin/activate
daphne -b 0.0.0.0 -p 8001 config.asgi:application
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/rooms/` | Create room |
| GET | `/api/rooms/{code}/` | Get room state |
| POST | `/api/rooms/{code}/join/` | Join room |
| POST | `/api/rooms/{code}/transfer-host/` | Transfer host to another participant |
| POST | `/api/rooms/{code}/queue/` | Add YouTube URL to queue (host only) |
| POST | `/api/rooms/{code}/skip/` | Skip current song (host only) |
| DELETE | `/api/rooms/{code}/queue/{id}/` | Remove from queue (host only) |
| POST | `/api/rooms/{code}/reactions/` | Send live reaction |
| POST | `/api/rooms/{code}/applause/` | Trigger virtual applause |

## WebSocket

`ws://localhost:8001/ws/rooms/{CODE}/`
