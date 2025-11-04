from django.db import models
from django.core.validators import EmailValidator
from website_config.models import SingletonModel


class LoyaltyProgram(SingletonModel):
    """
    Configuración del programa de fidelización (Singleton).
    """
    
    name = models.CharField(
        max_length=200,
        default='Club Kvernicola',
        verbose_name='Nombre del Club'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción del programa de fidelización'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Habilitar/deshabilitar el programa'
    )
    terms_and_conditions = models.TextField(
        blank=True,
        verbose_name='Términos y Condiciones',
        help_text='Términos y condiciones del programa'
    )
    
    # Beneficios (JSON para flexibilidad)
    benefits = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Beneficios',
        help_text='Lista de beneficios del club: [{"title": "...", "description": "...", "icon": "..."}]'
    )
    
    # Configuración de Puntos (opcional para futuras funcionalidades)
    points_enabled = models.BooleanField(
        default=False,
        verbose_name='Sistema de Puntos Habilitado'
    )
    points_per_euro = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
        verbose_name='Puntos por Euro Gastado'
    )
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')
    
    class Meta:
        verbose_name = 'Programa de Fidelización'
        verbose_name_plural = 'Programa de Fidelización'
    
    def __str__(self):
        return self.name


class ClubMember(models.Model):
    """
    Miembros del club de fidelización.
    """
    
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('suspended', 'Suspendido'),
    ]
    
    # Información Personal
    name = models.CharField(
        max_length=200,
        verbose_name='Nombre Completo'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        validators=[EmailValidator()]
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono'
    )
    
    # Código de Miembro
    member_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        verbose_name='Código de Miembro',
        help_text='Código único del miembro'
    )
    
    # Estado
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Estado'
    )
    
    # Puntos (si está habilitado)
    points_balance = models.PositiveIntegerField(
        default=0,
        verbose_name='Saldo de Puntos'
    )
    total_points_earned = models.PositiveIntegerField(
        default=0,
        verbose_name='Total de Puntos Ganados'
    )
    total_points_redeemed = models.PositiveIntegerField(
        default=0,
        verbose_name='Total de Puntos Canjeados'
    )
    
    # Preferencias de Comunicación
    accepts_email_marketing = models.BooleanField(
        default=True,
        verbose_name='Acepta Email Marketing'
    )
    accepts_sms_marketing = models.BooleanField(
        default=False,
        verbose_name='Acepta SMS Marketing'
    )
    
    # Fechas
    join_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Inscripción'
    )
    last_visit_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Última Visita'
    )
    
    # Metadatos
    notes = models.TextField(
        blank=True,
        verbose_name='Notas'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')
    
    class Meta:
        verbose_name = 'Miembro del Club'
        verbose_name_plural = 'Miembros del Club'
        ordering = ['-join_date']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['member_code']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f'{self.name} ({self.member_code})'
    
    def save(self, *args, **kwargs):
        # Generar código de miembro si no existe
        if not self.member_code:
            import uuid
            self.member_code = f'CLUB-{str(uuid.uuid4())[:8].upper()}'
        super().save(*args, **kwargs)
    
    def add_points(self, points, description=''):
        """Añade puntos al miembro."""
        self.points_balance += points
        self.total_points_earned += points
        self.save(update_fields=['points_balance', 'total_points_earned'])
        
        # Registrar transacción
        PointsTransaction.objects.create(
            member=self,
            transaction_type='earned',
            points=points,
            description=description
        )
    
    def redeem_points(self, points, description=''):
        """Canjea puntos del miembro."""
        if points > self.points_balance:
            raise ValueError('Saldo de puntos insuficiente')
        
        self.points_balance -= points
        self.total_points_redeemed += points
        self.save(update_fields=['points_balance', 'total_points_redeemed'])
        
        # Registrar transacción
        PointsTransaction.objects.create(
            member=self,
            transaction_type='redeemed',
            points=points,
            description=description
        )


class PointsTransaction(models.Model):
    """
    Historial de transacciones de puntos.
    """
    
    TRANSACTION_TYPES = [
        ('earned', 'Ganados'),
        ('redeemed', 'Canjeados'),
        ('expired', 'Expirados'),
        ('adjusted', 'Ajustados'),
    ]
    
    member = models.ForeignKey(
        ClubMember,
        on_delete=models.CASCADE,
        related_name='points_transactions',
        verbose_name='Miembro'
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        verbose_name='Tipo de Transacción'
    )
    points = models.IntegerField(
        verbose_name='Puntos',
        help_text='Cantidad de puntos (positivo o negativo)'
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Descripción'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    
    class Meta:
        verbose_name = 'Transacción de Puntos'
        verbose_name_plural = 'Transacciones de Puntos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.member.name} - {self.transaction_type} {self.points} pts'
