# 🎉 Backend de Operaciones - Microservicio Django

## ✅ Proyecto Completado

Se ha creado exitosamente el microservicio de operaciones con arquitectura de microservicios y las siguientes características:

## 📦 Estructura del Proyecto

```
backend-operaciones/
├── operations_service/          # Proyecto Django principal
│   ├── __init__.py             # Inicialización con Celery
│   ├── settings.py             # Configuración completa del proyecto
│   ├── celery.py               # Configuración de Celery
│   ├── urls.py                 # URLs principales con JWT
│   ├── wsgi.py                 # WSGI para producción
│   └── asgi.py                 # ASGI para async
│
├── suppliers/                   # App de Proveedores
│   ├── models.py               # Modelo Supplier con validación de RUT
│   ├── serializers.py          # Serializers DRF
│   ├── views.py                # ViewSets con CRUD completo
│   ├── urls.py                 # Rutas REST
│   └── admin.py                # Panel de administración
│
├── inventory/                   # App de Inventario
│   ├── models.py               # Category, UnitOfMeasure, Product, 
│   │                           # PurchaseUnit, Purchase, PurchaseItem
│   ├── serializers.py          # Serializers completos para todos los modelos
│   ├── views.py                # ViewSets con acciones personalizadas
│   ├── urls.py                 # Rutas REST organizadas
│   ├── tasks.py                # Tareas Celery (eventos, stock)
│   └── admin.py                # Panel de administración
│
├── recipes/                     # App de Recetas
│   ├── models.py               # Recipe, RecipeIngredient
│   ├── serializers.py          # Serializers con cálculo de costos
│   ├── views.py                # ViewSets con desglose de costos
│   ├── urls.py                 # Rutas REST
│   ├── tasks.py                # Tareas Celery (eventos)
│   └── admin.py                # Panel de administración
│
├── scripts/
│   └── init_data.py            # Script de inicialización de datos
│
├── requirements.txt             # Dependencias Python
├── Dockerfile                  # Imagen Docker
├── docker-compose.yml          # Orquestación completa
├── docker-entrypoint.sh        # Script de entrada
├── .env.example                # Variables de entorno
├── .gitignore                  # Archivos ignorados
├── .dockerignore               # Archivos ignorados en Docker
├── manage.py                   # CLI de Django
├── README.md                   # Documentación completa
├── QUICKSTART.md               # Guía de inicio rápido
├── COMMANDS.md                 # Comandos útiles
└── API_EXAMPLES.md             # Ejemplos de uso de API
```

## 🚀 Características Implementadas

### 1. Apps de Django

#### **Suppliers (Proveedores)**
- ✅ Modelo con validación de RUT chileno
- ✅ CRUD completo vía REST API
- ✅ Soft delete (marcado como inactivo)
- ✅ Filtros y búsqueda
- ✅ Endpoint para ver compras del proveedor

#### **Inventory (Inventario)**
- ✅ Categorías de productos
- ✅ Unidades de medida base (g, kg, L, ml, un)
- ✅ Unidades de compra con factores de conversión
- ✅ Productos con control de stock
- ✅ Compras con actualización automática de stock
- ✅ Cálculo automático de costo promedio ponderado
- ✅ Alertas de stock bajo
- ✅ Historial de movimientos

#### **Recipes (Recetas)**
- ✅ Recetas con ingredientes
- ✅ Cálculo automático de costos
- ✅ Costo por unidad de rendimiento
- ✅ Desglose detallado de costos
- ✅ Recalculación manual de costos
- ✅ Conversión de unidades

### 2. API REST (Django REST Framework)

#### **Autenticación**
- ✅ JWT (JSON Web Tokens)
- ✅ Token de acceso y refresh
- ✅ Endpoints: `/api/token/`, `/api/token/refresh/`

#### **Endpoints Principales**
```
/api/operations/suppliers/              # CRUD proveedores
/api/operations/inventory/categories/   # CRUD categorías
/api/operations/inventory/units/        # CRUD unidades
/api/operations/inventory/products/     # CRUD productos
/api/operations/inventory/purchases/    # CRUD compras
/api/operations/recipes/                # CRUD recetas
```

#### **Características de la API**
- ✅ Paginación automática
- ✅ Filtros por múltiples campos
- ✅ Búsqueda de texto completo
- ✅ Ordenamiento flexible
- ✅ Serializers optimizados (list vs detail)
- ✅ Acciones personalizadas (@action)
- ✅ Validación robusta

### 3. Lógica de Negocio

#### **Gestión de Compras**
1. ✅ Al registrar una compra:
   - Calcula costo neto (considera IVA según tipo de documento)
   - Convierte cantidades a unidades base
   - Actualiza stock del producto
   - Recalcula costo promedio ponderado
   - Publica evento `PRODUCT_STOCK_UPDATED`

#### **Gestión de Recetas**
1. ✅ Al crear/actualizar receta:
   - Calcula costo de cada ingrediente
   - Suma costo total
   - Calcula costo por unidad
   - Publica evento `RECIPE_UPDATED`

#### **Procesamiento de Ventas**
1. ✅ Al recibir evento `ORDEN_PAGADA` del POS:
   - Reduce stock de productos vendidos
   - Valida existencia de productos
   - Publica eventos de actualización

### 4. Sistema de Eventos (Celery + RabbitMQ)

#### **Tareas Implementadas**
- ✅ `publish_product_stock_updated` - Publica cambios de stock
- ✅ `process_order_paid` - Procesa órdenes del POS
- ✅ `listen_pos_events` - Escucha eventos del POS
- ✅ `check_low_stock_alerts` - Verifica stock bajo
- ✅ `publish_recipe_updated` - Publica cambios de recetas
- ✅ `recalculate_all_recipe_costs` - Recalcula costos masivos

#### **Eventos**
- ✅ Exchange: `operations_events` (topic)
- ✅ Exchange: `pos_events` (topic)
- ✅ Queue: `pos_orders_queue`
- ✅ Routing keys configurados

### 5. Dockerización Completa

#### **Servicios Docker Compose**
- ✅ `db_operaciones` - MariaDB 10.11
- ✅ `redis` - Redis 7 (backend de Celery)
- ✅ `event_bus` - RabbitMQ 3 con management
- ✅ `operations_service` - Django + Gunicorn
- ✅ `celery_worker` - Worker de Celery
- ✅ `celery_beat` - Beat para tareas programadas

#### **Características Docker**
- ✅ Health checks en todos los servicios
- ✅ Volúmenes persistentes
- ✅ Red compartida para microservicios
- ✅ Variables de entorno configurables
- ✅ Script de entrada inteligente
- ✅ Espera automática de dependencias

### 6. Configuración y Seguridad

- ✅ Variables de entorno (.env)
- ✅ Configuración separada dev/prod
- ✅ CORS configurado
- ✅ Autenticación JWT
- ✅ Validación de datos robusta
- ✅ Logging completo
- ✅ Manejo de errores

### 7. Documentación

- ✅ README.md completo
- ✅ QUICKSTART.md para inicio rápido
- ✅ COMMANDS.md con comandos útiles
- ✅ API_EXAMPLES.md con ejemplos de uso
- ✅ Comentarios en código
- ✅ Docstrings en funciones

## 🎯 Flujo de Trabajo Principal

### Escenario: Registrar una compra

1. **Usuario registra compra** → POST `/api/operations/inventory/purchases/`
2. **Sistema procesa**:
   - Guarda Purchase con PurchaseItems
   - Para cada item:
     - Calcula costo neto (considera IVA)
     - Convierte a unidades base
     - Actualiza stock del producto
     - Recalcula costo promedio
3. **Celery publica evento** → `PRODUCT_STOCK_UPDATED`
4. **Otros servicios** reciben el evento y actualizan sus datos

### Escenario: Recibir venta del POS

1. **POS publica evento** → `ORDEN_PAGADA`
2. **Celery escucha** → `listen_pos_events`
3. **Celery procesa** → `process_order_paid`
4. **Sistema actualiza**:
   - Reduce stock de productos vendidos
   - Publica evento de actualización
5. **Base de datos** refleja cambios en tiempo real

## 🔧 Tecnologías Utilizadas

- **Backend**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Base de Datos**: MySQL/MariaDB
- **Tareas Asíncronas**: Celery 5.3.4
- **Message Broker**: RabbitMQ
- **Cache/Results**: Redis
- **Autenticación**: JWT (djangorestframework-simplejwt)
- **CORS**: django-cors-headers
- **Servidor**: Gunicorn
- **Containerización**: Docker + Docker Compose

## 📊 Modelos de Base de Datos

### Suppliers
- `Supplier` - Información de proveedores

### Inventory
- `Category` - Categorías de productos
- `UnitOfMeasure` - Unidades base (g, L, un)
- `PurchaseUnit` - Unidades de compra (saco 25kg, bidón 5L)
- `Product` - Productos con stock y costo
- `Purchase` - Órdenes de compra
- `PurchaseItem` - Ítems de compra

### Recipes
- `Recipe` - Recetas con costos
- `RecipeIngredient` - Ingredientes de recetas

## 🚀 Cómo Empezar

### Opción 1: Docker (Recomendado)

```powershell
cd backend-operaciones
docker-compose up --build -d
```

Acceder a:
- API: http://localhost:8001/
- Admin: http://localhost:8001/admin/ (admin/admin123)
- RabbitMQ: http://localhost:15673/ (guest/guest)

### Opción 2: Local

```powershell
cd backend-operaciones
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Configurar .env
Copy-Item .env.example .env

# Iniciar servicios (MySQL, Redis, RabbitMQ)
docker-compose up -d db_operaciones redis event_bus

# Migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Inicializar datos
python manage.py shell < scripts/init_data.py

# Ejecutar
python manage.py runserver
celery -A operations_service worker -l info
```

## 📝 Próximos Pasos Sugeridos

1. **Testing**: Agregar tests unitarios y de integración
2. **API Gateway**: Configurar gateway para exponer las APIs
3. **Frontend**: Conectar con aplicación web/móvil
4. **Monitoreo**: Agregar Prometheus/Grafana
5. **CI/CD**: Pipeline de despliegue automático
6. **Backup**: Sistema de backups automáticos
7. **Notificaciones**: Alertas de stock bajo por email/SMS
8. **Reportes**: Endpoints de reportes y estadísticas

## 🎓 Recursos de Aprendizaje

- Ver ejemplos en `API_EXAMPLES.md`
- Consultar comandos en `COMMANDS.md`
- Seguir guía rápida en `QUICKSTART.md`
- Leer documentación completa en `README.md`

## ✨ Características Destacadas

1. **Arquitectura Limpia**: Separación clara de responsabilidades
2. **Escalabilidad**: Diseñado para crecer con microservicios
3. **Mantenibilidad**: Código bien documentado y organizado
4. **Performance**: Caché, paginación, queries optimizados
5. **Seguridad**: Autenticación JWT, validación robusta
6. **DevOps Ready**: Docker, logs, health checks
7. **Event-Driven**: Comunicación asíncrona entre servicios
8. **Real-Time**: Actualizaciones en tiempo real vía eventos

## 🎉 ¡Listo para Usar!

El microservicio está completamente funcional y listo para:
- ✅ Desarrollo local
- ✅ Despliegue con Docker
- ✅ Integración con otros microservicios
- ✅ Producción (con ajustes de configuración)

---

**Contacto**: Equipo de Desarrollo
**Fecha**: Octubre 2025
**Versión**: 1.0.0
