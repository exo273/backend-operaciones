from django.contrib import admin
from .models import Supplier, SupplierCategory


@admin.register(SupplierCategory)
class SupplierCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'suppliers_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def suppliers_count(self, obj):
        return obj.suppliers.count()
    suppliers_count.short_description = 'Cantidad de Proveedores'


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'rut', 'category', 'contact_person', 'phone', 'email', 'city', 'is_active']
    list_filter = ['is_active', 'category', 'city', 'region']
    search_fields = ['name', 'rut', 'contact_person', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('name', 'rut', 'category', 'is_active')
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
