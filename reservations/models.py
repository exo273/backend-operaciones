from django.db import models
from django.core.validators import EmailValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone


class Reservation(models.Model):
    """
    Reservas del restaurante realizadas desde la web.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
        ('completed', 'Completada'),
        ('no_show', 'No se presentó'),
    ]
    
    # Información del Cliente
    name = models.CharField(
        max_length=200,
        verbose_name='Nombre Completo'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Teléfono'
    )
    email = models.EmailField(
        verbose_name='Email',
        validators=[EmailValidator()]
    )
    
    # Detalles de la Reserva
    date = models.DateField(
        verbose_name='Fecha',
        help_text='Fecha de la reserva'
    )
    time = models.TimeField(
        verbose_name='Hora',
        help_text='Hora de la reserva'
    )
    guests = models.PositiveIntegerField(
        verbose_name='Número de Comensales',
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    
    # Información Adicional
    special_requests = models.TextField(
        blank=True,
        verbose_name='Peticiones Especiales',
        help_text='Alergias, preferencias de mesa, celebraciones, etc.'
    )
    
    # Estado y Gestión
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Estado'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Notas Internas',
        help_text='Notas del personal (no visibles para el cliente)'
    )
    
    # Confirmación
    confirmation_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Código de Confirmación',
        help_text='Código único de confirmación'
    )
    confirmed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Confirmada el'
    )
    confirmed_by = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Confirmada por'
    )
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizada')
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name='IP',
        help_text='IP desde donde se hizo la reserva'
    )
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['-date', '-time']),
            models.Index(fields=['status']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f'{self.name} - {self.date} {self.time} ({self.guests} personas)'
    
    def save(self, *args, **kwargs):
        # Generar código de confirmación si no existe
        if not self.confirmation_code:
            import uuid
            self.confirmation_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)
    
    def is_past(self):
        """Verifica si la reserva ya pasó."""
        reservation_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time)
        )
        return reservation_datetime < timezone.now()
    
    def confirm(self, confirmed_by='Sistema'):
        """Marca la reserva como confirmada."""
        self.status = 'confirmed'
        self.confirmed_at = timezone.now()
        self.confirmed_by = confirmed_by
        self.save(update_fields=['status', 'confirmed_at', 'confirmed_by'])
    
    def cancel(self):
        """Cancela la reserva."""
        self.status = 'cancelled'
        self.save(update_fields=['status'])
