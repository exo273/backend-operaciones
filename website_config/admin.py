from django.contrib import admin
from .models import WebsiteSettings, GalleryImage


@admin.register(WebsiteSettings)
class WebsiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Información Básica', {
            'fields': ('site_name', 'tagline')
        }),
        ('Header', {
            'fields': ('header_text', 'logo')
        }),
        ('Footer', {
            'fields': ('footer_text', 'footer_copyright')
        }),
        ('Colores y Diseño', {
            'fields': ('primary_color', 'secondary_color', 'accent_color'),
            'classes': ('collapse',)
        }),
        ('Información de Contacto', {
            'fields': ('phone', 'whatsapp', 'email', 'address')
        }),
        ('Horarios', {
            'fields': ('opening_hours',),
            'description': 'Formato JSON: {"lunes": "12:00-16:00, 20:00-23:00", "martes": "Cerrado"}'
        }),
        ('Redes Sociales', {
            'fields': ('social_links',),
            'description': 'Formato JSON: {"facebook": "url", "instagram": "url", "twitter": "url"}'
        }),
        ('Ubicación', {
            'fields': ('google_maps_embed', 'latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Páginas Visibles', {
            'fields': ('visible_pages',),
            'description': 'Formato JSON: {"home": true, "gallery": false, ...}'
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords', 'google_analytics_id'),
            'classes': ('collapse',)
        }),
        ('Anuncios', {
            'fields': ('announcement_active', 'announcement_text')
        }),
        ('Configuración del Menú', {
            'fields': ('menu_title', 'menu_description', 'menu_footer_text'),
            'classes': ('collapse',)
        }),
        ('Reservas', {
            'fields': ('reservations_enabled', 'reservations_email', 'max_guests_per_reservation'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir una instancia
        return not WebsiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar la configuración
        return False


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_featured', 'is_active')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'description')
        }),
        ('Categorización', {
            'fields': ('category', 'order', 'is_featured', 'is_active')
        }),
        ('Metadatos', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
