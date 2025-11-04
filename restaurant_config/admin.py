from django.contrib import admin
from .models import RestaurantConfig


@admin.register(RestaurantConfig)
class RestaurantConfigAdmin(admin.ModelAdmin):
    """
    Admin para RestaurantConfig
    No permite crear múltiples instancias
    """
    def has_add_permission(self, request):
        # Solo permite agregar si no existe ninguna instancia
        return not RestaurantConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permite eliminar
        return False
    
    list_display = ['name', 'currency_symbol', 'language', 'updated_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'logo', 'receipt_logo')
        }),
        ('Localización', {
            'fields': ('currency_symbol', 'language')
        }),
        ('Contacto', {
            'fields': ('address', 'phone', 'email', 'website'),
            'classes': ('collapse',)
        }),
    )
