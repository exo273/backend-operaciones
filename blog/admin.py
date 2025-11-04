from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'is_featured', 'published_date', 'views_count', 'created_at')
    list_filter = ('status', 'category', 'is_featured', 'published_date', 'created_at')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'is_featured')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'slug', 'excerpt')
        }),
        ('Contenido', {
            'fields': ('content', 'featured_image')
        }),
        ('Autor', {
            'fields': ('author', 'author_name')
        }),
        ('Publicación', {
            'fields': ('status', 'is_featured', 'published_date')
        }),
        ('Categorización', {
            'fields': ('category', 'tags')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Estadísticas', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Si es un nuevo post y no tiene autor, asignar el usuario actual
        if not change and not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
