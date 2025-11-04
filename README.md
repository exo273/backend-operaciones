# Backend de Operaciones - Sistema de Gestión

Microservicio de operaciones para la gestión de proveedores, inventario, recetas y CMS del sitio web.

## 🏗️ Arquitectura

Este servicio forma parte de una arquitectura de microservicios y maneja:

### Gestión Interna
- **Proveedores**: Gestión de información de proveedores
- **Inventario**: Control de productos, categorías, unidades de medida y stock
- **Recetas**: Definición de recetas con cálculo automático de costos

### CMS y Website Público
- **Website Config**: Configuración global del sitio web (colores, contacto, horarios, SEO)
- **Blog**: Sistema de blog con slugs automáticos, categorías, tags y contador de vistas
- **Galería**: Gestión de imágenes con categorías y destacados
- **Páginas Legales**: Privacidad, cookies, términos y condiciones
- **Reservas**: Sistema de reservas online con confirmaciones automáticas
- **Club de Fidelización**: Programa de puntos y beneficios para clientes

### APIs
- **APIs Internas**: Endpoints autenticados para el panel de administración
- **APIs Públicas**: Endpoints sin autenticación para el frontend del website

## 🛠️ Tecnologías

- **Django 4.2.7**: Framework web
- **Django REST Framework**: API REST
- **MySQL/MariaDB**: Base de datos relacional
- **Celery**: Tareas asíncronas y procesamiento de eventos
- **RabbitMQ**: Message broker para eventos entre microservicios
- **Redis**: Backend de resultados de Celery
- **Docker**: Containerización

## � Módulos Django

Este servicio está organizado en 8 aplicaciones Django:

### Apps de Gestión Interna
1. **suppliers**: Gestión de proveedores y contactos
2. **inventory**: Productos, categorías, unidades de medida y stock
3. **recipes**: Recetas con ingredientes y cálculo de costos

### Apps del CMS (Nuevas en v2.0)
4. **website_config**: Configuración global del sitio + galería de imágenes
   - Modelo `WebsiteSettings` (Singleton): URL, colores, contacto, horarios, SEO
   - Modelo `GalleryImage`: Imágenes con categorías y orden
5. **blog**: Sistema de blog completo
   - Modelo `BlogPost`: Posts con slugs automáticos, categorías, tags, SEO
6. **legal**: Páginas legales
   - Modelo `LegalPage`: Privacidad, cookies, términos, GDPR
7. **reservations**: Sistema de reservas online
   - Modelo `Reservation`: Reservas con confirmaciones y estados
8. **loyalty_club**: Programa de fidelización
   - Modelo `LoyaltyProgram` (Singleton): Configuración del programa
   - Modelo `ClubMember`: Miembros con códigos únicos y puntos
   - Modelo `PointsTransaction`: Historial de transacciones

## �📋 Requisitos Previos

- Python 3.11+
- MySQL/MariaDB
- RabbitMQ
- Redis
- Docker y Docker Compose (recomendado)

## 🚀 Instalación Local

### 1. Clonar el repositorio y configurar entorno

```powershell
# Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copiar `.env.example` a `.env` y configurar:

```powershell
Copy-Item .env.example .env
```

Editar `.env` con tus credenciales:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta
DB_HOST=localhost
DB_PORT=3306
DB_NAME=db_operaciones
DB_USER=root
DB_PASS=tu_password
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672
```

### 3. Crear base de datos

```sql
CREATE DATABASE db_operaciones CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Aplicar migraciones

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Inicializar configuración del website (Nuevo en v2.0)

```powershell
python manage.py init_website_config
```

Este comando crea:
- Configuración inicial del sitio web (WebsiteSettings)
- Programa de fidelización predeterminado (LoyaltyProgram)

### 6. Crear superusuario

```powershell
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```powershell
# Servidor de desarrollo
python manage.py runserver

# En otra terminal, ejecutar Celery worker
celery -A operations_service worker -l info

# (Opcional) Celery Beat para tareas programadas
celery -A operations_service beat -l info
```

## 🐳 Instalación con Docker

```powershell
# Construir imagen
docker build -t operations-service .

# Ejecutar con Docker Compose (recomendado)
docker-compose up -d
```

## 📡 Endpoints API

### Autenticación

```
POST /api/token/                    # Obtener token JWT
POST /api/token/refresh/            # Refrescar token
```

### APIs Internas (Requieren Autenticación)

#### Proveedores

```
GET    /api/operations/suppliers/           # Listar proveedores
POST   /api/operations/suppliers/           # Crear proveedor
GET    /api/operations/suppliers/{id}/      # Detalle de proveedor
PUT    /api/operations/suppliers/{id}/      # Actualizar proveedor
DELETE /api/operations/suppliers/{id}/      # Eliminar proveedor
POST   /api/operations/suppliers/{id}/activate/  # Reactivar proveedor
GET    /api/operations/suppliers/{id}/purchases/ # Compras del proveedor
```

#### Inventario

**Categorías**
```
GET    /api/operations/inventory/categories/      # Listar categorías
POST   /api/operations/inventory/categories/      # Crear categoría
```

**Unidades de Medida**
```
GET    /api/operations/inventory/units/           # Listar unidades
POST   /api/operations/inventory/units/           # Crear unidad
```

**Productos**
```
GET    /api/operations/inventory/products/        # Listar productos
POST   /api/operations/inventory/products/        # Crear producto
GET    /api/operations/inventory/products/{id}/   # Detalle de producto
PUT    /api/operations/inventory/products/{id}/   # Actualizar producto
GET    /api/operations/inventory/products/low_stock/  # Productos con stock bajo
GET    /api/operations/inventory/products/{id}/stock_history/  # Historial de stock
```

#### Recetas

```
GET    /api/operations/recipes/                   # Listar recetas
POST   /api/operations/recipes/                   # Crear receta
GET    /api/operations/recipes/{id}/              # Detalle de receta
PUT    /api/operations/recipes/{id}/              # Actualizar receta
POST   /api/operations/recipes/{id}/recalculate_cost/  # Recalcular costo
POST   /api/operations/recipes/{id}/add_ingredient/    # Agregar ingrediente
GET    /api/operations/recipes/{id}/cost_breakdown/    # Desglose de costos
```

### APIs Públicas del Website (Sin Autenticación)

> 📚 **Documentación completa**: Ver [WEBSITE_API_README.md](./WEBSITE_API_README.md)

#### Configuración y Contenido
```
GET    /api/website/config/            # Configuración del sitio web
GET    /api/website/gallery/           # Galería de imágenes (filtrable)
GET    /api/website/menu/              # Menú público con productos activos
```

#### Blog
```
GET    /api/website/blog/              # Listar posts publicados (filtrable)
GET    /api/website/blog/{slug}/       # Detalle de post (incrementa vistas)
```

#### Páginas Legales
```
GET    /api/website/legal/             # Listar páginas legales
GET    /api/website/legal/{slug}/      # Contenido de página legal
```

#### Reservas
```
POST   /api/website/reservations/      # Crear nueva reserva
```

#### Club de Fidelización
```
GET    /api/website/loyalty-program/   # Info del programa
POST   /api/website/loyalty-club/join/ # Inscribirse al club
```

## 🔄 Sistema de Eventos

### Eventos Publicados

1. **PRODUCT_STOCK_UPDATED**: Se dispara cuando cambia el stock de un producto
   - Routing key: `product.stock.updated`
   - Datos: `product_id`, `new_stock`, `new_cost`

2. **RECIPE_UPDATED**: Se dispara cuando se actualiza una receta
   - Routing key: `recipe.updated`
   - Datos: `recipe_id`, `recipe_name`, `total_cost`, `cost_per_unit`

### Eventos Consumidos

1. **ORDEN_PAGADA** (desde servicio POS)
   - Queue: `pos_orders_queue`
   - Routing key: `order.paid`
   - Acción: Reduce el stock de los productos vendidos

## 🗂️ Estructura del Proyecto

```
backend-operaciones/
├── operations_service/       # Configuración del proyecto Django
│   ├── __init__.py
│   ├── settings.py          # Configuración principal
│   ├── celery.py            # Configuración de Celery
│   ├── urls.py              # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── suppliers/               # App de proveedores
│   ├── models.py           # Modelo Supplier
│   ├── serializers.py      # Serializers DRF
│   ├── views.py            # ViewSets
│   ├── urls.py
│   └── admin.py
├── inventory/              # App de inventario
│   ├── models.py          # Modelos: Category, UnitOfMeasure, Product, Purchase, etc.
│   ├── serializers.py     # Serializers DRF
│   ├── views.py           # ViewSets
│   ├── urls.py
│   ├── tasks.py           # Tareas de Celery
│   └── admin.py
├── recipes/               # App de recetas
│   ├── models.py         # Modelos: Recipe, RecipeIngredient
│   ├── serializers.py    # Serializers DRF
│   ├── views.py          # ViewSets
│   ├── urls.py
│   ├── tasks.py          # Tareas de Celery
│   └── admin.py
├── requirements.txt       # Dependencias Python
├── Dockerfile            # Imagen Docker
├── docker-entrypoint.sh  # Script de entrada
├── .env.example          # Ejemplo de variables de entorno
└── manage.py            # CLI de Django
```

## 💼 Lógica de Negocio Clave

### Gestión de Compras y Stock

Cuando se registra una compra:

1. Se calcula el costo neto por unidad base (considerando IVA según tipo de documento)
2. Se actualiza el stock del producto sumando la cantidad comprada
3. Se recalcula el costo promedio ponderado del producto
4. Se publica un evento `PRODUCT_STOCK_UPDATED` al bus de eventos

### Gestión de Recetas

Cuando se crea/actualiza una receta:

1. Se calculan los costos de cada ingrediente basándose en:
   - Cantidad necesaria del ingrediente
   - Factor de conversión a unidad base
   - Costo promedio actual del producto
2. Se suma el costo total de todos los ingredientes
3. Se calcula el costo por unidad de rendimiento
4. Se publica un evento `RECIPE_UPDATED` al bus de eventos

### Procesamiento de Ventas (desde POS)

Cuando se recibe un evento de orden pagada:

1. Se valida que todos los productos existan
2. Se reduce el stock de cada producto vendido
3. Se publica un evento de actualización de stock por cada producto

## 🔐 Autenticación

El servicio usa JWT (JSON Web Tokens) para autenticación:

```python
# Obtener token
POST /api/token/
{
    "username": "admin",
    "password": "password123"
}

# Respuesta
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# Usar el token en requests
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 🧪 Testing

```powershell
# Ejecutar tests
python manage.py test

# Con cobertura
coverage run --source='.' manage.py test
coverage report
```

## 📊 Panel de Administración

Acceder a `/admin/` con las credenciales de superusuario para gestionar datos directamente.

## 🔧 Comandos Útiles

```powershell
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar shell interactivo
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic

# Verificar problemas
python manage.py check
```

## 📝 Notas de Desarrollo

### Agregar nueva funcionalidad

1. Crear modelos en `models.py`
2. Crear migraciones: `python manage.py makemigrations`
3. Crear serializers en `serializers.py`
4. Crear ViewSets en `views.py`
5. Registrar rutas en `urls.py`
6. Agregar al admin en `admin.py`

### Tareas asíncronas con Celery

Las tareas se definen en `tasks.py` de cada app:

```python
@shared_task
def mi_tarea_asincrona(param):
    # Lógica de la tarea
    pass

# Ejecutar
mi_tarea_asincrona.delay(valor)
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto es privado y propietario.

## 👥 Contacto

Para consultas sobre el proyecto, contactar al equipo de desarrollo.
