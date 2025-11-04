from django.contrib import admin
from .models import LegalPage


@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_type', 'is_active', 'order', 'updated_at')
    list_filter = ('page_type', 'is_active')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'slug', 'page_type')
        }),
        ('Contenido', {
            'fields': ('content',)
        }),
        ('Configuración', {
            'fields': ('is_active', 'order')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
