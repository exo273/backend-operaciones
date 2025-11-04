"""
Modelo Singleton para configuración global del restaurante
"""
from django.db import models
from django.core.exceptions import ValidationError


class SingletonModel(models.Model):
    """
    Modelo abstracto que asegura que solo exista una instancia
    """
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


class RestaurantConfig(SingletonModel):
    """
    Configuración global del restaurante (Singleton)
    Solo puede existir una instancia de este modelo
    """
    name = models.CharField(
        max_length=255,
        default="Mi Restaurante",
        verbose_name='Nombre del Restaurante',
        help_text='Nombre comercial del establecimiento'
    )
    logo = models.ImageField(
        upload_to='branding/',
        null=True,
        blank=True,
        verbose_name='Logo Principal',
        help_text='Logo para el panel de administración'
    )
    receipt_logo = models.ImageField(
        upload_to='branding/',
        null=True,
        blank=True,
        verbose_name='Logo para Comandas',
        help_text='Logo simplificado para impresión en comandas'
    )
    currency_symbol = models.CharField(
        max_length=5,
        default="S/",
        verbose_name='Símbolo de Moneda',
        help_text='Símbolo de la moneda utilizada (ej. $, S/, €)'
    )
    language = models.CharField(
        max_length=10,
        default='es',
        verbose_name='Idioma',
        help_text='Código de idioma del sistema'
    )
    
    # Información adicional de contacto
    address = models.TextField(
        blank=True,
        verbose_name='Dirección',
        help_text='Dirección física del establecimiento'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono',
        help_text='Teléfono de contacto'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='Email',
        help_text='Email de contacto'
    )
    website = models.URLField(
        blank=True,
        verbose_name='Sitio Web',
        help_text='URL del sitio web'
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        db_table = 'restaurant_config'
        verbose_name = 'Configuración del Restaurante'
        verbose_name_plural = 'Configuración del Restaurante'
    
    def __str__(self):
        return self.name
