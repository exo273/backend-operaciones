from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date',
        'time',
        'guests',
        'phone',
        'status_badge',
        'is_past_due',
        'created_at'
    )
    list_filter = ('status', 'date', 'guests', 'created_at')
    search_fields = ('name', 'phone', 'email', 'confirmation_code')
    list_editable = ('status',)
    readonly_fields = ('confirmation_code', 'created_at', 'updated_at', 'ip_address', 'confirmed_at', 'confirmed_by')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('name', 'phone', 'email')
        }),
        ('Detalles de la Reserva', {
            'fields': ('date', 'time', 'guests', 'special_requests')
        }),
        ('Estado y Gestión', {
            'fields': ('status', 'notes')
        }),
        ('Confirmación', {
            'fields': ('confirmation_code', 'confirmed_at', 'confirmed_by'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at', 'ip_address'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['confirm_reservations', 'cancel_reservations']
    
    def status_badge(self, obj):
        """Muestra un badge de color según el estado."""
        colors = {
            'pending': 'orange',
            'confirmed': 'green',
            'cancelled': 'red',
            'completed': 'blue',
            'no_show': 'gray',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Estado'
    
    def is_past_due(self, obj):
        """Indica si la reserva ya pasó."""
        if obj.is_past():
            return format_html('<span style="color: red;">✗ Pasada</span>')
        return format_html('<span style="color: green;">✓ Futura</span>')
    is_past_due.short_description = 'Vigencia'
    
    def confirm_reservations(self, request, queryset):
        """Acción para confirmar múltiples reservas."""
        count = 0
        for reservation in queryset:
            if reservation.status == 'pending':
                reservation.confirm(confirmed_by=request.user.email)
                count += 1
        self.message_user(request, f'{count} reserva(s) confirmada(s).')
    confirm_reservations.short_description = 'Confirmar reservas seleccionadas'
    
    def cancel_reservations(self, request, queryset):
        """Acción para cancelar múltiples reservas."""
        count = queryset.update(status='cancelled')
        self.message_user(request, f'{count} reserva(s) cancelada(s).')
    cancel_reservations.short_description = 'Cancelar reservas seleccionadas'
