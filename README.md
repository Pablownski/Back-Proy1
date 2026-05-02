# GOAT Ranker — API

REST API for rating and ranking footballers. Built with FastAPI, PostgreSQL, and Docker.

## Stack

- **FastAPI** + Uvicorn
- **PostgreSQL 15** via SQLAlchemy
- **Docker Compose**

## Requirements

- Docker + Docker Compose

## Setup

```bash
cp .env.example .env
# Edit .env with your credentials
```

## Run

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| API | http://localhost:8001 |
| Docs (Swagger) | http://localhost:8001/docs |
| PostgreSQL (pgAdmin) | localhost:5433 |

## Environment Variables

```env
POSTGRES_USER=rank
POSTGRES_PASSWORD=cr7thegoat
POSTGRES_DB=goatdb
DATABASE_URL=postgresql://rank:cr7thegoat@db:5432/goatdb
API_PORT=8001
DB_EXTERNAL_PORT=5433
```

## API Endpoints

### Players
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/players` | List players — supports `?q=`, `?page=`, `?limit=`, `?sort=`, `?order=` |
| `GET` | `/players/{id}` | Get player by ID |
| `POST` | `/players` | Create player (multipart/form-data) |
| `PUT` | `/players/{id}` | Update player |
| `DELETE` | `/players/{id}` | Delete player |

### Ratings
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/players/{id}/ratings` | Add rating (score 1–10) |
| `GET` | `/players/{id}/ratings` | Get all ratings for a player |

### Ranking
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/ranking` | Get full tier list grouped by tier |
| `POST` | `/ranking` | Add player to ranking |
| `PUT` | `/ranking/{id}` | Update ranking entry (tier / position) |
| `DELETE` | `/ranking/{id}` | Remove player from ranking |

## pgAdmin Connection

| Field | Value |
|-------|-------|
| Host | `localhost` |
| Port | `5433` |
| Database | `goatdb` |
| Username | `rank` |
| Password | `cr7thegoat` |

## Image Uploads

Images are stored in `./uploads/` and served at `/uploads/<filename>`.  
Max size: 1 MB. Accepted formats: JPG, PNG.
