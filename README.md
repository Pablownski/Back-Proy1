# GOAT Ranker — Backend API

API REST para calificar y rankear futbolistas.
El servidor expone datos en formato JSON y es consumido por un cliente construido en JavaScript vanilla.

## Arquitectura

```
[ Frontend (HTML + JS) ]
        ↓ fetch()
[ Backend API (FastAPI) ]
        ↓
[ PostgreSQL Database ]
```

- El backend **no genera HTML**
- El frontend **no accede directamente** a la base de datos
- La comunicación se realiza mediante **HTTP + JSON**

## Tecnologías

- **FastAPI** — framework backend
- **PostgreSQL** — base de datos
- **SQLAlchemy** — ORM
- **Docker & Docker Compose**
- **Uvicorn** — servidor ASGI

## Configuración

Clonar el repositorio y configurar variables de entorno:

```bash
cp .env.example .env
```

Variables en `.env`:

```env
POSTGRES_USER=rank
POSTGRES_PASSWORD=cr7thegoat
POSTGRES_DB=goatdb
DATABASE_URL=postgresql://rank:cr7thegoat@db:5432/goatdb
API_PORT=8001
DB_EXTERNAL_PORT=5433
```

## Ejecución con Docker

```bash
docker compose up --build
```

## Endpoints

### Players (Jugadores)

| Método | Endpoint | Descripción | Status |
|--------|----------|-------------|--------|
| GET | `/players` | Listar jugadores | 200 |
| GET | `/players/{id}` | Obtener jugador por ID | 200 / 404 |
| POST | `/players` | Crear jugador (multipart) | 201 |
| PUT | `/players/{id}` | Actualizar jugador | 200 / 404 |
| DELETE | `/players/{id}` | Eliminar jugador | 204 / 404 |

Query params disponibles en `GET /players`:

| Param | Valores | Descripción |
|-------|---------|-------------|
| `?q=` | texto | Búsqueda por nombre |
| `?page=` | número | Número de página |
| `?limit=` | número | Resultados por página |
| `?sort=` | `name` \| `rating` | Campo de ordenamiento |
| `?order=` | `asc` \| `desc` | Dirección del ordenamiento |

### Ratings

| Método | Endpoint | Descripción | Status |
|--------|----------|-------------|--------|
| POST | `/players/{id}/ratings` | Agregar calificación (1–10) | 201 / 404 |
| GET | `/players/{id}/ratings` | Obtener calificaciones y promedio | 200 / 404 |

### Ranking (Tier List)

| Método | Endpoint | Descripción | Status |
|--------|----------|-------------|--------|
| GET | `/ranking` | Obtener tier list agrupada por tier | 200 |
| POST | `/ranking` | Agregar jugador al ranking | 201 / 400 / 404 |
| PUT | `/ranking/{id}` | Actualizar tier o posición | 200 / 404 |
| DELETE | `/ranking` | Eliminar todos los jugadores del ranking | 200 |
| DELETE | `/ranking/{id}` | Eliminar un jugador del ranking | 204 / 404 |

La respuesta de `GET /ranking` incluye `ranking_id` por jugador, lo que permite al frontend hacer DELETE individuales sin estado adicional.

## Imágenes

- Se suben al crear jugadores (`POST /players`, multipart/form-data)
- Formatos permitidos: JPG, PNG
- Tamaño máximo: 1 MB
- Se almacenan en el volumen Docker `proy1_uploads`
- Acceso público: `/uploads/<filename>`

## CORS

El navegador bloquea peticiones entre distintos orígenes (puertos distintos cuentan como orígenes distintos). Esto se llama **CORS** (Cross-Origin Resource Sharing).

El backend está configurado para permitir todos los orígenes:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

## Códigos HTTP

| Código | Significado |
|--------|-------------|
| 200 | Éxito |
| 201 | Recurso creado |
| 204 | Eliminado sin contenido |
| 400 | Error de validación |
| 404 | Recurso no encontrado |

## Documentación interactiva

Swagger UI disponible en `/docs` (servido directamente por el backend).
OpenAPI spec en `/openapi.json`.

## Base de datos

PostgreSQL corre en Docker:

| Campo | Valor |
|-------|-------|
| Host | localhost |
| Port | 5433 |
| DB | goatdb |
| User | rank |

## Frontend

El cliente está en un repositorio separado:

[https://github.com/Pablownski/Frontend-Proy1](https://github.com/Pablownski/Frontend-Proy1)

## Estado del proyecto

- CRUD completo de jugadores
- Paginación, búsqueda y ordenamiento
- Sistema de rating (tabla propia, endpoints propios)
- Tier ranking con bulk delete
- Subida y servido de imágenes
- Swagger UI y OpenAPI spec
- Dockerizado con volumen persistente para imágenes
