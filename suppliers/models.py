"""
Modelos de la aplicación Suppliers.
Gestiona la información de proveedores.
"""

from django.db import models
from django.core.validators import RegexValidator


class SupplierCategory(models.Model):
    """Categoría de proveedor."""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría de Proveedor"
        verbose_name_plural = "Categorías de Proveedores"
        ordering = ['name']

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """Proveedor de productos."""
    
    # Validador para RUT chileno (formato: 12345678-9)
    rut_validator = RegexValidator(
        regex=r'^\d{7,8}-[\dkK]$',
        message='RUT debe estar en formato 12345678-9 o 12345678-K'
    )
    
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Nombre o Razón Social"
    )
    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[rut_validator],
        verbose_name="RUT",
        help_text="Formato: 12345678-9"
    )
    category = models.ForeignKey(
        SupplierCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='suppliers',
        verbose_name="Categoría"
    )
    contact_person = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Persona de Contacto"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Teléfono"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Correo Electrónico"
    )
    address = models.TextField(
        blank=True,
        verbose_name="Dirección"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Ciudad"
    )
    region = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Región"
    )
    website = models.URLField(
        blank=True,
        verbose_name="Sitio Web"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notas"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['rut']),
            models.Index(fields=['is_active']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.name} ({self.rut})"

    def clean(self):
        """Validación adicional del RUT."""
        from django.core.exceptions import ValidationError
        
        if self.rut:
            # Limpiar el RUT
            rut = self.rut.replace('.', '').replace('-', '')
            
            if len(rut) < 2:
                raise ValidationError({'rut': 'RUT inválido'})
            
            # Separar número y dígito verificador
            numero = rut[:-1]
            dv = rut[-1].upper()
            
            # Validar que el número sea numérico
            if not numero.isdigit():
                raise ValidationError({'rut': 'RUT debe contener solo números antes del guión'})
            
            # Calcular dígito verificador
            suma = 0
            multiplicador = 2
            
            for d in reversed(numero):
                suma += int(d) * multiplicador
                multiplicador += 1
                if multiplicador > 7:
                    multiplicador = 2
            
            resto = suma % 11
            dv_calculado = 11 - resto
            
            if dv_calculado == 11:
                dv_esperado = '0'
            elif dv_calculado == 10:
                dv_esperado = 'K'
            else:
                dv_esperado = str(dv_calculado)
            
            if dv != dv_esperado:
                raise ValidationError({'rut': f'Dígito verificador incorrecto. Debería ser {dv_esperado}'})
