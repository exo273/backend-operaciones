# Website API Documentation

APIs públicas para el sitio web (SvelteKit frontend).

## Características

- ✅ **Sin autenticación requerida** - Endpoints públicos para consumo del frontend
- ✅ **CORS habilitado** - Configurado para kvernicola.cl (personalizable desde WebsiteSettings)
- ✅ **Datos centralizados** - Misma base de datos que POS y panel de administración
- ✅ **SEO optimizado** - Meta tags, slugs únicos, sitemap
- ✅ **Imágenes optimizadas** - Soporte para imágenes en productos, galería y blog
- ✅ **URL personalizable** - El dominio del sitio se configura desde el panel de administración

---

## Endpoints Disponibles

### 1. Configuración del Sitio

**GET** `/api/website/config/`

Obtiene toda la configuración pública del sitio web.

**Response:**
```json
{
  "id": 1,
  "site_name": "Kvernicola",
  "site_url": "https://www.kvernicola.cl",
  "tagline": "Sabores Auténticos, Momentos Inolvidables",
  "logo_url": "https://api.kvernicola.cl/media/logos/logo.png",
  "header_text": "Bienvenidos",
  "footer_text": "© 2025 Kvernicola",
  "primary_color": "#FF6B35",
  "secondary_color": "#004E89",
  "accent_color": "#F7931E",
  "phone": "+34 XXX XXX XXX",
  "whatsapp": "+34 XXX XXX XXX",
  "email": "info@kvernicola.com",
  "address": "Calle Principal, 123",
  "opening_hours": {
    "monday": "Cerrado",
    "tuesday": "12:00 - 16:00, 20:00 - 23:00",
    ...
  },
  "social_links": {
    "facebook": "https://facebook.com/kvernicola",
    "instagram": "https://instagram.com/kvernicola"
  },
  "visible_pages": {
    "home": true,
    "menu": true,
    "gallery": true,
    "blog": true,
    ...
  },
  "meta_description": "Restaurante K'Vernicola...",
  "google_analytics_id": "G-XXXXXXXXXX",
  ...
}
```

---

### 2. Galería de Imágenes

**GET** `/api/website/gallery/`

Lista todas las imágenes activas de la galería.

**Query Params:**
- `category` (opcional): Filtrar por categoría (ej: "platos", "ambiente", "eventos")
- `featured` (opcional): Solo imágenes destacadas (`true`/`false`)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Paella de Mariscos",
    "image_url": "https://api.kvernicola.cl/media/gallery/paella.jpg",
    "description": "Nuestra especialidad de la casa",
    "category": "platos",
    "is_featured": true,
    "created_at": "2024-01-15T10:00:00Z"
  },
  ...
]
```

---

### 3. Menú Web

**GET** `/api/website/menu/`

Obtiene el menú completo con productos activos para la web.

**Query Params:**
- `category` (opcional): Filtrar por ID de categoría

**Response:**
```json
{
  "menu_title": "Nuestro Menú",
  "menu_description": "Platos elaborados con ingredientes frescos...",
  "menu_footer_text": "Todos los precios incluyen IVA",
  "categories": [
    {
      "id": 1,
      "name": "Entrantes",
      "description": "Para empezar"
    },
    ...
  ],
  "products": [
    {
      "id": 1,
      "name": "Croquetas Caseras",
      "category_name": "Entrantes",
      "description_display": "Croquetas artesanales de jamón ibérico",
      "web_price": "8.50",
      "image_url": "https://api.kvernicola.cl/media/products/croquetas.jpg",
      "is_available": true,
      "allergens": ["gluten", "lactosa"]
    },
    ...
  ]
}
```

---

### 4. Blog

#### Listar Posts

**GET** `/api/website/blog/`

Lista posts publicados del blog.

**Query Params:**
- `category` (opcional): Filtrar por categoría
- `tag` (opcional): Filtrar por tag
- `search` (opcional): Buscar en título/contenido
- `featured` (opcional): Solo posts destacados (`true`/`false`)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Nueva Carta de Verano",
    "slug": "nueva-carta-de-verano",
    "excerpt_display": "Descubre nuestra nueva selección de platos frescos...",
    "featured_image_url": "https://api.kvernicola.cl/media/blog/verano.jpg",
    "author_name": "Chef María",
    "published_date": "2024-06-01T12:00:00Z",
    "category": "Novedades",
    "tags": ["menu", "verano", "temporada"],
    "views_count": 150,
    "is_featured": true
  },
  ...
]
```

#### Detalle de Post

**GET** `/api/website/blog/{slug}/`

Obtiene el detalle completo de un post. **Incrementa automáticamente el contador de vistas.**

**Response:**
```json
{
  "id": 1,
  "title": "Nueva Carta de Verano",
  "slug": "nueva-carta-de-verano",
  "content": "<p>Contenido completo del post en HTML...</p>",
  "featured_image_url": "https://api.kvernicola.cl/media/blog/verano.jpg",
  "author_name": "Chef María",
  "published_date": "2024-06-01T12:00:00Z",
  "category": "Novedades",
  "tags": ["menu", "verano", "temporada"],
  "meta_description": "SEO description...",
  "views_count": 151,
  "created_at": "2024-05-28T10:00:00Z"
}
```

---

### 5. Páginas Legales

#### Listar Páginas

**GET** `/api/website/legal/`

Lista todas las páginas legales activas.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Política de Privacidad",
    "slug": "politica-de-privacidad",
    "page_type": "privacy",
    "updated_at": "2024-01-10T12:00:00Z"
  },
  ...
]
```

#### Detalle de Página

**GET** `/api/website/legal/{slug}/`

Obtiene el contenido completo de una página legal.

**Response:**
```json
{
  "id": 1,
  "title": "Política de Privacidad",
  "slug": "politica-de-privacidad",
  "page_type": "privacy",
  "content": "<h1>Política de Privacidad</h1><p>...</p>",
  "meta_description": "Política de privacidad de K'Vernicola",
  "updated_at": "2024-01-10T12:00:00Z"
}
```

---

### 6. Reservas

**POST** `/api/website/reservations/`

Crea una nueva reserva desde el sitio web.

**Request Body:**
```json
{
  "name": "Juan Pérez",
  "phone": "+34 600 000 000",
  "email": "juan@example.com",
  "date": "2024-07-15",
  "time": "20:30:00",
  "guests": 4,
  "special_requests": "Mesa junto a la ventana si es posible"
}
```

**Response (201 Created):**
```json
{
  "id": 42,
  "confirmation_code": "ABCD1234",
  "name": "Juan Pérez",
  "date": "2024-07-15",
  "time": "20:30:00",
  "guests": 4,
  "status": "pending",
  "message": "Reserva creada exitosamente. Recibirás una confirmación por email."
}
```

**Validaciones:**
- El número de comensales debe estar entre 1 y el máximo configurado (por defecto 10)
- Las reservas deben estar habilitadas en la configuración del sitio
- Se captura automáticamente la IP del cliente

---

### 7. Club de Fidelización

#### Información del Programa

**GET** `/api/website/loyalty-program/`

Obtiene información pública del programa de fidelización.

**Response:**
```json
{
  "id": 1,
  "name": "Club K'Vernicola",
  "description": "Únete a nuestro club de fidelización...",
  "is_active": true,
  "benefits": [
    {
      "title": "Descuentos Exclusivos",
      "description": "10% de descuento en todos tus pedidos",
      "icon": "tag"
    },
    ...
  ],
  "points_enabled": true,
  "points_per_euro": 10,
  "terms_and_conditions": "Los puntos caducan..."
}
```

#### Unirse al Club

**POST** `/api/website/loyalty-club/join/`

Inscribe un nuevo miembro al club de fidelización.

**Request Body:**
```json
{
  "name": "Ana García",
  "email": "ana@example.com",
  "phone": "+34 600 000 000",
  "accepts_email_marketing": true,
  "accepts_sms_marketing": false
}
```

**Response (201 Created):**
```json
{
  "id": 15,
  "member_code": "CLUB-A3F8B2E1",
  "name": "Ana García",
  "email": "ana@example.com",
  "status": "active",
  "points_balance": 0,
  "join_date": "2024-06-15T14:30:00Z",
  "message": "¡Bienvenido al Club K'Vernicola! Tu código de miembro es CLUB-A3F8B2E1"
}
```

**Validaciones:**
- El email debe ser único
- El programa debe estar activo
- Se genera automáticamente un código de miembro único

---

## Configuración Inicial

### 1. Instalar dependencias

```bash
cd backend-operaciones
pip install -r requirements.txt
```

### 2. Crear migraciones

```bash
python manage.py makemigrations website_config blog legal reservations loyalty_club inventory
python manage.py migrate
```

### 3. Inicializar configuración

```bash
python manage.py init_website_config
```

Este comando crea:
- ✅ Configuración inicial del sitio web (WebsiteSettings)
- ✅ Programa de fidelización predeterminado (LoyaltyProgram)

### 4. Crear superusuario (si no existe)

```bash
python manage.py createsuperuser
```

### 5. Configurar productos para la web

Desde el panel de administración (`/admin/`):

1. Ve a **Inventory → Products**
2. Edita cada producto que quieras mostrar en la web
3. Marca el checkbox **Is active website**
4. Completa los campos web:
   - **Description web**: Descripción optimizada para la web
   - **Image**: Sube una imagen del producto
   - **Web price**: Precio de venta al público
   - **Display order**: Orden de visualización (menor = primero)

---

## CORS Configuration

Asegúrate de tener configurado CORS en `settings.py`:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

# Para desarrollo
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # SvelteKit dev server
    "http://localhost:4173",  # SvelteKit preview
]

# Para producción - Usar el dominio configurado en WebsiteSettings
CORS_ALLOWED_ORIGINS = [
    "https://www.kvernicola.cl",
    "https://kvernicola.cl",
]

# Alternativamente, permitir subdominios dinámicamente
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.kvernicola\.cl$",
]
```

**Nota**: El dominio (`kvernicola.cl`) es personalizable desde el panel de administración en **Website Config → Site URL**. Asegúrate de que el dominio en CORS coincida con el configurado.

---

## Media Files Configuration

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# urls.py (solo en desarrollo)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

En producción, configura Nginx para servir archivos estáticos:

```nginx
location /media/ {
    alias /app/media/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

---

## Próximos Pasos

1. **Frontend SvelteKit**
   - Crear proyecto en `website-frontend/`
   - Instalar Skeleton UI + Tailwind CSS
   - Implementar páginas: Home, Menu, Gallery, Blog, Reservations, Loyalty Club
   - Configurar variables de entorno para API URLs (usar el dominio de WebsiteSettings)

2. **Email Notifications**
   - Configurar SMTP en Django settings
   - Enviar emails de confirmación de reservas
   - Emails de bienvenida al club de fidelización

3. **SEO Optimization**
   - Implementar sitemap.xml dinámico (usar site_url de WebsiteSettings)
   - robots.txt
   - Meta tags Open Graph (usar site_url como og:url base)
   - Google Analytics integration

4. **Nginx Configuration**
   - Configurar routing para el dominio personalizado (kvernicola.cl)
   - SSL/HTTPS certificates
   - Rate limiting para APIs públicas
   - Configurar subdominios (www.kvernicola.cl, api.kvernicola.cl)

---

## Notas Técnicas

### SingletonModel Pattern

Los modelos `WebsiteSettings` y `LoyaltyProgram` usan el patrón Singleton:

```python
# Siempre obtener la instancia única
settings = WebsiteSettings.load()
program = LoyaltyProgram.load()

# NO crear nuevas instancias manualmente
```

### Auto-generación de Códigos

- **Blog/Legal slugs**: Se generan automáticamente desde el título
- **Confirmation codes**: UUID aleatorio de 8 caracteres (ej: `ABCD1234`)
- **Member codes**: Formato `CLUB-XXXXXXXX` (8 caracteres hex)

### JSON Fields

Varios modelos usan `JSONField` para flexibilidad:
- `opening_hours`: Horarios por día de la semana
- `social_links`: URLs de redes sociales
- `benefits`: Lista de beneficios del club
- `tags`: Etiquetas del blog

---

## Soporte

Para dudas o problemas, revisar:
- Logs del servidor: `docker-compose logs -f backend-operations`
- Panel de administración: `/admin/`
- Django Debug Toolbar (en desarrollo)

---

**Versión:** 2.0.0  
**Última actualización:** Octubre 2025

**Dominio configurado**: kvernicola.cl (Chile)  
**URL personalizable desde**: Panel Admin → Website Config → Site URL
