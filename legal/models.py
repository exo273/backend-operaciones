from django.db import models
from django.utils.text import slugify


class LegalPage(models.Model):
    """
    Páginas legales del sitio web.
    Política de Privacidad, Cookies, Términos y Condiciones, etc.
    """
    
    PAGE_TYPES = [
        ('privacy', 'Política de Privacidad'),
        ('cookies', 'Política de Cookies'),
        ('terms', 'Términos y Condiciones'),
        ('gdpr', 'Información GDPR'),
        ('legal_notice', 'Aviso Legal'),
        ('other', 'Otra'),
    ]
    
    title = models.CharField(
        max_length=300,
        verbose_name='Título'
    )
    slug = models.SlugField(
        max_length=350,
        unique=True,
        verbose_name='Slug',
        help_text='URL amigable'
    )
    page_type = models.CharField(
        max_length=50,
        choices=PAGE_TYPES,
        default='other',
        verbose_name='Tipo de Página'
    )
    content = models.TextField(
        verbose_name='Contenido',
        help_text='Soporta HTML o Markdown'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activa',
        help_text='Mostrar en el sitio web'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de aparición en el footer'
    )
    
    # SEO
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        verbose_name='Meta Descripción'
    )
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    class Meta:
        verbose_name = 'Página Legal'
        verbose_name_plural = 'Páginas Legales'
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
