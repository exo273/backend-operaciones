from django.db import models
from django.utils.text import slugify
from django.conf import settings


class BlogPost(models.Model):
    """Publicaciones del blog del restaurante."""
    
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
        ('archived', 'Archivado'),
    ]
    
    title = models.CharField(
        max_length=300,
        verbose_name='Título'
    )
    slug = models.SlugField(
        max_length=350,
        unique=True,
        verbose_name='Slug',
        help_text='URL amigable (se genera automáticamente si se deja vacío)'
    )
    excerpt = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Extracto',
        help_text='Resumen corto del artículo (opcional)'
    )
    content = models.TextField(
        verbose_name='Contenido',
        help_text='Soporta Markdown o HTML'
    )
    featured_image = models.ImageField(
        upload_to='blog/featured/',
        blank=True,
        null=True,
        verbose_name='Imagen Destacada'
    )
    
    # Autor
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_posts',
        verbose_name='Autor'
    )
    author_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nombre del Autor',
        help_text='Se muestra este nombre si no hay usuario asociado'
    )
    
    # Estado y Publicación
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Estado'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Destacado',
        help_text='Aparece en la portada'
    )
    published_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Fecha de Publicación'
    )
    
    # Categorías y Etiquetas
    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Categoría',
        help_text='Ejemplo: "Recetas", "Noticias", "Eventos"'
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Etiquetas',
        help_text='Lista de etiquetas: ["cocina", "tradicional", "tips"]'
    )
    
    # SEO
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        verbose_name='Meta Descripción',
        help_text='Para SEO (máx. 160 caracteres)'
    )
    
    # Estadísticas
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Vistas'
    )
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')
    
    class Meta:
        verbose_name = 'Artículo del Blog'
        verbose_name_plural = 'Artículos del Blog'
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Generar slug automáticamente si no existe
        if not self.slug:
            self.slug = slugify(self.title)
            # Asegurar que el slug sea único
            original_slug = self.slug
            counter = 1
            while BlogPost.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Si no hay author_name y hay autor, usar el nombre del usuario
        if not self.author_name and self.author:
            if hasattr(self.author, 'get_full_name'):
                self.author_name = self.author.get_full_name() or self.author.email
            else:
                self.author_name = str(self.author)
        
        super().save(*args, **kwargs)
    
    def get_author_display(self):
        """Retorna el nombre del autor para mostrar."""
        if self.author_name:
            return self.author_name
        if self.author:
            if hasattr(self.author, 'get_full_name'):
                return self.author.get_full_name() or self.author.email
            return str(self.author)
        return 'Anónimo'
    
    def increment_views(self):
        """Incrementa el contador de vistas."""
        self.views_count += 1
        self.save(update_fields=['views_count'])
