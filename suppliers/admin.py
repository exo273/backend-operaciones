from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'rut', 'contact_person', 'phone', 'email', 'city', 'is_active']
    list_filter = ['is_active', 'city', 'region']
    search_fields = ['name', 'rut', 'contact_person', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('name', 'rut', 'is_active')
        }),
        ('Contacto', {
            'fields': ('contact_person', 'phone', 'email')
        }),
        ('Ubicación', {
            'fields': ('address', 'city', 'region')
        }),
        ('Adicional', {
            'fields': ('website', 'notes')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
