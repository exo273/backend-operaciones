from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class SingletonModel(models.Model):
    """Clase base para modelos que solo deben tener una instancia."""
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class WebsiteSettings(SingletonModel):
    """
    Configuración global del sitio web (Singleton).
    Solo puede existir una instancia de este modelo.
    """
    # Información Básica
    site_name = models.CharField(
        max_length=200,
        default='Kvernicola',
        verbose_name='Nombre del Sitio'
    )
    site_url = models.URLField(
        max_length=255,
        default='https://www.kvernicola.com',
        verbose_name='URL del Sitio',
        help_text='URL completa del sitio web (ej: https://www.kvernicola.com)'
    )
    tagline = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Eslogan',
        help_text='Ejemplo: "Cocina tradicional con sabor casero"'
    )
    
    # Header
    header_text = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Texto del Header',
        help_text='Texto que aparece en la parte superior de todas las páginas'
    )
    logo = models.ImageField(
        upload_to='website/logos/',
        blank=True,
        null=True,
        verbose_name='Logo'
    )
    
    # Footer
    footer_text = models.TextField(
        blank=True,
        verbose_name='Texto del Footer',
        help_text='Texto que aparece en el pie de página'
    )
    footer_copyright = models.CharField(
        max_length=200,
        default='© 2024 Kvernicola. Todos los derechos reservados.',
        verbose_name='Texto de Copyright'
    )
    
    # Colores y Diseño
    primary_color = models.CharField(
        max_length=7,
        default='#e74c3c',
        verbose_name='Color Primario',
        help_text='Formato: #RRGGBB'
    )
    secondary_color = models.CharField(
        max_length=7,
        default='#2c3e50',
        verbose_name='Color Secundario',
        help_text='Formato: #RRGGBB'
    )
    accent_color = models.CharField(
        max_length=7,
        default='#f39c12',
        verbose_name='Color de Acento',
        help_text='Formato: #RRGGBB'
    )
    
    # Información de Contacto
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono'
    )
    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='WhatsApp',
        help_text='Número en formato internacional: +34612345678'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='Email de Contacto'
    )
    address = models.TextField(
        blank=True,
        verbose_name='Dirección'
    )
    
    # Horarios
    opening_hours = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Horarios de Apertura',
        help_text='Ejemplo: {"lunes": "12:00-16:00, 20:00-23:00", "martes": "Cerrado"}'
    )
    
    # Redes Sociales
    social_links = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Enlaces de Redes Sociales',
        help_text='Ejemplo: {"facebook": "https://facebook.com/...", "instagram": "https://instagram.com/..."}'
    )
    
    # Ubicación (Mapa)
    google_maps_embed = models.TextField(
        blank=True,
        verbose_name='Código Embed de Google Maps',
        help_text='Código iframe de Google Maps'
    )
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
        verbose_name='Latitud'
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
        verbose_name='Longitud'
    )
    
    # Páginas Visibles
    visible_pages = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Páginas Visibles',
        help_text='Controla qué páginas se muestran en el menú'
    )
    
    # SEO
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        verbose_name='Meta Descripción',
        help_text='Descripción que aparece en los resultados de búsqueda (máx. 160 caracteres)'
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Meta Keywords',
        help_text='Palabras clave separadas por comas'
    )
    google_analytics_id = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='ID de Google Analytics',
        help_text='Ejemplo: G-XXXXXXXXXX o UA-XXXXXXXXX-X'
    )
    
    # Avisos y Banners
    announcement_text = models.TextField(
        blank=True,
        verbose_name='Texto de Anuncio',
        help_text='Banner informativo que aparece en el sitio'
    )
    announcement_active = models.BooleanField(
        default=False,
        verbose_name='Anuncio Activo'
    )
    
    # Configuración del Menú Web
    menu_title = models.CharField(
        max_length=200,
        default='Menú de Hoy',
        verbose_name='Título del Menú'
    )
    menu_description = models.TextField(
        blank=True,
        verbose_name='Descripción del Menú',
        help_text='Texto introductorio para la página del menú'
    )
    menu_footer_text = models.TextField(
        blank=True,
        verbose_name='Texto al pie del Menú',
        help_text='Ejemplo: "Todos los precios incluyen IVA"'
    )
    
    # Configuración de Reservas
    reservations_enabled = models.BooleanField(
        default=True,
        verbose_name='Reservas Habilitadas'
    )
    reservations_email = models.EmailField(
        blank=True,
        verbose_name='Email para Notificaciones de Reservas'
    )
    max_guests_per_reservation = models.PositiveIntegerField(
        default=10,
        verbose_name='Máximo de Comensales por Reserva'
    )
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    class Meta:
        verbose_name = 'Configuración del Sitio Web'
        verbose_name_plural = 'Configuración del Sitio Web'
    
    def __str__(self):
        return f'Configuración de {self.site_name}'
    
    def get_visible_pages(self):
        """Retorna las páginas que deben mostrarse en el menú."""
        default_pages = {
            'home': True,
            'menu': True,
            'how_to_get_there': True,
            'gallery': True,
            'blog': False,
            'loyalty_club': False,
            'reservations': True,
        }
        return {**default_pages, **self.visible_pages}


class GalleryImage(models.Model):
    """Imágenes para la galería del sitio web."""
    
    title = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    image = models.ImageField(
        upload_to='website/gallery/',
        verbose_name='Imagen'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Categoría',
        help_text='Ejemplo: "Platos", "Restaurante", "Eventos"'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de visualización (menor primero)'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Destacada',
        help_text='Aparece en portada o carrusel'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activa'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    
    class Meta:
        verbose_name = 'Imagen de Galería'
        verbose_name_plural = 'Imágenes de Galería'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
