⚽ GOAT Ranker — Backend API

API REST para calificar y rankear futbolistas.
El servidor expone datos en formato JSON y es consumido por un cliente construido en JavaScript vanilla.

🧠 Arquitectura

Este proyecto sigue una arquitectura desacoplada:

[ Frontend (HTML + JS) ]
            ↓ fetch()
[ Backend API (FastAPI) ]
            ↓
[ PostgreSQL Database ]
El backend NO genera HTML
El frontend NO accede directamente a la base de datos
La comunicación se realiza mediante HTTP + JSON
🚀 Tecnologías
FastAPI — framework backend
PostgreSQL — base de datos
SQLAlchemy — ORM
Docker & Docker Compose
Uvicorn — servidor ASGI
⚙️ Configuración

Clonar el repositorio y configurar variables de entorno:

cp .env.example .env

Editar .env según sea necesario:

POSTGRES_USER=rank
POSTGRES_PASSWORD=cr7thegoat
POSTGRES_DB=goatdb
DATABASE_URL=postgresql://rank:cr7thegoat@db:5432/goatdb
API_PORT=8001
DB_EXTERNAL_PORT=5433
🐳 Ejecución con Docker
docker compose up --build
🌐 Endpoints disponibles
📌 Players (Futbolistas)
Método	Endpoint	Descripción
GET	/players	Listar jugadores (soporta filtros)
GET	/players/{id}	Obtener jugador por ID
POST	/players	Crear jugador
PUT	/players/{id}	Actualizar jugador
DELETE	/players/{id}	Eliminar jugador
🔍 Query Params soportados
?q=         búsqueda por nombre
?page=      número de página
?limit=     resultados por página
?sort=      name | rating
?order=     asc | desc
⭐ Ratings
Método	Endpoint	Descripción
POST	/players/{id}/ratings	Agregar calificación (1–10)
GET	/players/{id}/ratings	Obtener calificaciones
🏆 Ranking (Tier List)
Método	Endpoint	Descripción
GET	/ranking	Obtener tier list
POST	/ranking	Agregar jugador al ranking
PUT	/ranking/{id}	Actualizar tier/posición
DELETE	/ranking/{id}	Eliminar del ranking
🖼️ Manejo de imágenes
Se pueden subir imágenes al crear jugadores
Formatos permitidos: JPG, PNG
Tamaño máximo: 1 MB
Las imágenes se almacenan en /uploads

Acceso:

/uploads/<filename>
🔐 CORS

El navegador bloquea peticiones entre distintos orígenes por seguridad.
Esto se conoce como CORS (Cross-Origin Resource Sharing).

Se configuró el backend para permitir todos los orígenes durante desarrollo:

Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type
📊 Códigos HTTP

La API utiliza códigos correctos:

200 → éxito
201 → recurso creado
204 → eliminado sin contenido
400 → error de validación
404 → recurso no encontrado
📚 Documentación interactiva

Swagger UI disponible en:

http://localhost:8001/docs
🗄️ Base de datos

PostgreSQL corre en Docker:

Campo	Valor
Host	localhost
Port	5433
DB	goatdb
User	rank
🔗 Frontend

El cliente está en un repositorio separado:

👉 (https://github.com/Pablownski/Frontend-Proy1)

🧪 Estado del proyecto

✔ CRUD completo
✔ Paginación
✔ Búsqueda
✔ Ordenamiento
✔ Sistema de rating
✔ Tier ranking
✔ Subida de imágenes
✔ Dockerizado

🧠 Notas

Este proyecto demuestra:

separación cliente-servidor
diseño de API REST
manejo de estado desde frontend
uso de base de datos real
consumo de API con fetch()