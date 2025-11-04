# Comandos Útiles de Desarrollo - Backend Operaciones

## Docker Compose

### Iniciar todos los servicios
```powershell
docker-compose up -d
```

### Ver logs en tiempo real
```powershell
# Todos los servicios
docker-compose logs -f

# Un servicio específico
docker-compose logs -f operations_service
docker-compose logs -f celery_worker
```

### Detener servicios
```powershell
docker-compose down
```

### Reconstruir imágenes
```powershell
docker-compose up --build -d
```

### Reiniciar un servicio
```powershell
docker-compose restart operations_service
```

### Ver estado de servicios
```powershell
docker-compose ps
```

### Eliminar todo (incluyendo volúmenes)
```powershell
docker-compose down -v
```

## Django Management

### Ejecutar comandos de Django en contenedor
```powershell
docker-compose exec operations_service python manage.py [comando]
```

### Crear y aplicar migraciones
```powershell
docker-compose exec operations_service python manage.py makemigrations
docker-compose exec operations_service python manage.py migrate
```

### Crear superusuario
```powershell
docker-compose exec operations_service python manage.py createsuperuser
```

### Shell de Django
```powershell
docker-compose exec operations_service python manage.py shell
```

### Shell de Python
```powershell
docker-compose exec operations_service python
```

### Inicializar datos básicos
```powershell
docker-compose exec operations_service python manage.py shell < scripts/init_data.py
```

### Ver configuración
```powershell
docker-compose exec operations_service python manage.py diffsettings
```

### Verificar problemas
```powershell
docker-compose exec operations_service python manage.py check
```

### Recolectar archivos estáticos
```powershell
docker-compose exec operations_service python manage.py collectstatic --noinput
```

## Celery

### Inspeccionar workers activos
```powershell
docker-compose exec celery_worker celery -A operations_service inspect active
```

### Ver tareas registradas
```powershell
docker-compose exec celery_worker celery -A operations_service inspect registered
```

### Ver workers conectados
```powershell
docker-compose exec celery_worker celery -A operations_service inspect stats
```

### Purgar todas las tareas pendientes
```powershell
docker-compose exec celery_worker celery -A operations_service purge
```

### Revocar una tarea
```powershell
docker-compose exec celery_worker celery -A operations_service revoke [task_id]
```

## Base de Datos

### Acceder al shell de MySQL
```powershell
docker-compose exec db_operaciones mysql -u operations_user -p db_operaciones
```

### Backup de base de datos
```powershell
docker-compose exec db_operaciones mysqldump -u operations_user -p db_operaciones > backup.sql
```

### Restaurar backup
```powershell
Get-Content backup.sql | docker-compose exec -T db_operaciones mysql -u operations_user -p db_operaciones
```

### Ver tablas
```sql
SHOW TABLES;
```

### Ver estructura de una tabla
```sql
DESCRIBE inventory_product;
```

## Redis

### Acceder al CLI de Redis
```powershell
docker-compose exec redis redis-cli
```

### Comandos útiles en Redis
```redis
# Ver todas las keys
KEYS *

# Ver el valor de una key
GET key_name

# Limpiar todas las keys
FLUSHALL

# Info del servidor
INFO
```

## RabbitMQ

### Acceder a Management UI
Abrir en navegador: http://localhost:15673
- Usuario: guest
- Password: guest

### Ver queues
```powershell
docker-compose exec event_bus rabbitmqctl list_queues
```

### Ver exchanges
```powershell
docker-compose exec event_bus rabbitmqctl list_exchanges
```

### Ver bindings
```powershell
docker-compose exec event_bus rabbitmqctl list_bindings
```

## Testing

### Ejecutar todos los tests
```powershell
docker-compose exec operations_service python manage.py test
```

### Ejecutar tests de una app específica
```powershell
docker-compose exec operations_service python manage.py test inventory
docker-compose exec operations_service python manage.py test suppliers
docker-compose exec operations_service python manage.py test recipes
```

### Ejecutar tests con verbosidad
```powershell
docker-compose exec operations_service python manage.py test --verbosity=2
```

### Ejecutar tests con cobertura
```powershell
docker-compose exec operations_service coverage run --source='.' manage.py test
docker-compose exec operations_service coverage report
docker-compose exec operations_service coverage html
```

## Debugging

### Ver variables de entorno
```powershell
docker-compose exec operations_service env
```

### Ver configuración de Django
```powershell
docker-compose exec operations_service python manage.py shell -c "from django.conf import settings; print(settings.DATABASES)"
```

### Entrar al contenedor
```powershell
docker-compose exec operations_service bash
```

### Ver logs de error de Django
```powershell
docker-compose exec operations_service tail -f operations_service.log
```

## API Testing con curl

### Obtener token JWT
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:8001/api/token/" -Method Post -Body (@{username="admin";password="admin123"} | ConvertTo-Json) -ContentType "application/json"
$token = $response.access
```

### Listar productos
```powershell
$headers = @{Authorization="Bearer $token"}
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/" -Headers $headers
```

### Crear categoría
```powershell
$headers = @{Authorization="Bearer $token"}
$body = @{name="Nueva Categoría";description="Descripción"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/categories/" -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

## Mantenimiento

### Limpiar containers detenidos
```powershell
docker container prune
```

### Limpiar imágenes sin usar
```powershell
docker image prune
```

### Limpiar todo el sistema Docker
```powershell
docker system prune -a
```

### Ver uso de espacio
```powershell
docker system df
```

## Desarrollo Local (sin Docker)

### Activar entorno virtual
```powershell
.\venv\Scripts\Activate.ps1
```

### Instalar dependencias
```powershell
pip install -r requirements.txt
```

### Ejecutar servidor de desarrollo
```powershell
python manage.py runserver 0.0.0.0:8001
```

### Ejecutar Celery worker
```powershell
celery -A operations_service worker -l info --pool=solo
```

### Ejecutar Celery beat
```powershell
celery -A operations_service beat -l info
```

## Monitoreo

### Ver uso de recursos de contenedores
```powershell
docker stats
```

### Ver uso de recursos de un contenedor específico
```powershell
docker stats operations_service
```

### Inspeccionar un contenedor
```powershell
docker inspect operations_service
```

## Git

### Ver estado
```powershell
git status
```

### Agregar cambios
```powershell
git add .
```

### Commit
```powershell
git commit -m "Mensaje del commit"
```

### Ver diferencias
```powershell
git diff
```

### Ver log
```powershell
git log --oneline
```
