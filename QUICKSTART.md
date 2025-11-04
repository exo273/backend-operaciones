# Guía de Inicio Rápido - Backend de Operaciones

## Inicio Rápido con Docker

### 1. Clonar y configurar

```powershell
cd c:\Users\raimu\OneDrive\Documents\gestion\backend-operaciones

# Copiar archivo de configuración
Copy-Item .env.example .env
```

### 2. Editar .env (opcional para desarrollo local)

El archivo `docker-compose.yml` ya tiene las variables configuradas. Solo necesitas editar `.env` si ejecutas sin Docker.

### 3. Iniciar servicios

```powershell
# Construir e iniciar todos los servicios
docker-compose up --build -d

# Ver logs
docker-compose logs -f operations_service

# Ver estado de servicios
docker-compose ps
```

### 4. Acceder a la aplicación

- **API REST**: http://localhost:8001/
- **Admin Django**: http://localhost:8001/admin/
  - Usuario: `admin`
  - Password: `admin123` (creado automáticamente)
- **RabbitMQ Management**: http://localhost:15673/
  - Usuario: `guest`
  - Password: `guest`

### 5. Probar la API

#### Obtener token JWT

```powershell
curl -X POST http://localhost:8001/api/token/ `
  -H "Content-Type: application/json" `
  -d '{"username":"admin","password":"admin123"}'
```

#### Listar productos

```powershell
$token = "tu-token-aqui"
curl -H "Authorization: Bearer $token" http://localhost:8001/api/operations/inventory/products/
```

## Comandos Útiles

### Docker Compose

```powershell
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Ver logs
docker-compose logs -f [servicio]

# Reiniciar un servicio
docker-compose restart operations_service

# Ejecutar comando en contenedor
docker-compose exec operations_service python manage.py shell

# Ver estado
docker-compose ps
```

### Django Management Commands

```powershell
# Crear migraciones
docker-compose exec operations_service python manage.py makemigrations

# Aplicar migraciones
docker-compose exec operations_service python manage.py migrate

# Crear superusuario
docker-compose exec operations_service python manage.py createsuperuser

# Shell de Django
docker-compose exec operations_service python manage.py shell

# Cargar datos de ejemplo
docker-compose exec operations_service python manage.py loaddata fixtures/initial_data.json
```

### Celery

```powershell
# Ver workers activos
docker-compose exec celery_worker celery -A operations_service inspect active

# Ver tareas registradas
docker-compose exec celery_worker celery -A operations_service inspect registered

# Purgar todas las tareas pendientes
docker-compose exec celery_worker celery -A operations_service purge
```

## Desarrollo Local (sin Docker)

### 1. Configurar entorno virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configurar servicios externos

Necesitas tener corriendo localmente:
- MySQL/MariaDB en puerto 3306
- Redis en puerto 6379
- RabbitMQ en puerto 5672

O usar los servicios de Docker Compose:

```powershell
# Solo iniciar las dependencias
docker-compose up -d db_operaciones redis event_bus
```

### 3. Configurar .env

```env
DEBUG=True
DB_HOST=localhost
DB_PORT=3306
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672
```

### 4. Ejecutar servidor

```powershell
# Terminal 1: Django
python manage.py runserver

# Terminal 2: Celery Worker
celery -A operations_service worker -l info

# Terminal 3: Celery Beat (opcional)
celery -A operations_service beat -l info
```

## Datos de Ejemplo

### Crear categorías iniciales

```python
# Ejecutar en shell de Django
from inventory.models import Category, UnitOfMeasure

# Categorías
Category.objects.create(name="Lácteos", description="Productos lácteos")
Category.objects.create(name="Carnes", description="Carnes y embutidos")
Category.objects.create(name="Verduras", description="Verduras y hortalizas")
Category.objects.create(name="Abarrotes", description="Productos secos")

# Unidades de medida
UnitOfMeasure.objects.create(name="Gramo", abbreviation="g")
UnitOfMeasure.objects.create(name="Litro", abbreviation="L")
UnitOfMeasure.objects.create(name="Unidad", abbreviation="un")
UnitOfMeasure.objects.create(name="Kilogramo", abbreviation="kg")
```

## Solución de Problemas

### Error de conexión a la base de datos

```powershell
# Verificar que el contenedor esté corriendo
docker-compose ps

# Ver logs de la base de datos
docker-compose logs db_operaciones

# Reiniciar servicio
docker-compose restart db_operaciones
```

### Error con Celery

```powershell
# Ver logs del worker
docker-compose logs celery_worker

# Reiniciar worker
docker-compose restart celery_worker

# Purgar tareas pendientes
docker-compose exec celery_worker celery -A operations_service purge
```

### Resetear todo

```powershell
# Detener y eliminar contenedores, volúmenes
docker-compose down -v

# Reconstruir desde cero
docker-compose up --build -d
```

## Endpoints Principales

### Autenticación
- `POST /api/token/` - Obtener token
- `POST /api/token/refresh/` - Refrescar token

### Proveedores
- `GET /api/operations/suppliers/` - Listar
- `POST /api/operations/suppliers/` - Crear

### Productos
- `GET /api/operations/inventory/products/` - Listar
- `POST /api/operations/inventory/products/` - Crear
- `GET /api/operations/inventory/products/low_stock/` - Stock bajo

### Compras
- `GET /api/operations/inventory/purchases/` - Listar
- `POST /api/operations/inventory/purchases/` - Registrar compra

### Recetas
- `GET /api/operations/recipes/` - Listar
- `POST /api/operations/recipes/` - Crear
- `GET /api/operations/recipes/{id}/cost_breakdown/` - Desglose

## Próximos Pasos

1. Explorar el panel de administración en `/admin/`
2. Crear proveedores, productos y categorías
3. Registrar compras para actualizar stock
4. Crear recetas y ver cálculos de costos
5. Revisar la documentación completa en `README.md`
