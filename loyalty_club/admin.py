from django.contrib import admin
from django.utils.html import format_html
from .models import LoyaltyProgram, ClubMember, PointsTransaction


@admin.register(LoyaltyProgram)
class LoyaltyProgramAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Beneficios', {
            'fields': ('benefits',),
            'description': 'Formato JSON: [{"title": "Descuento", "description": "10% en tu próxima compra", "icon": "🎁"}]'
        }),
        ('Sistema de Puntos', {
            'fields': ('points_enabled', 'points_per_euro'),
            'classes': ('collapse',)
        }),
        ('Términos', {
            'fields': ('terms_and_conditions',),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Solo permitir una instancia
        return not LoyaltyProgram.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


class PointsTransactionInline(admin.TabularInline):
    model = PointsTransaction
    extra = 0
    readonly_fields = ('transaction_type', 'points', 'description', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'member_code',
        'email',
        'phone',
        'status',
        'status_badge',
        'points_balance',
        'join_date'
    )
    list_filter = ('status', 'accepts_email_marketing', 'join_date')
    search_fields = ('name', 'email', 'phone', 'member_code')
    list_editable = ('status',)
    readonly_fields = ('member_code', 'join_date', 'created_at', 'updated_at', 'total_points_earned', 'total_points_redeemed')
    date_hierarchy = 'join_date'
    inlines = [PointsTransactionInline]
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Membresía', {
            'fields': ('member_code', 'status', 'join_date')
        }),
        ('Puntos', {
            'fields': ('points_balance', 'total_points_earned', 'total_points_redeemed')
        }),
        ('Preferencias de Comunicación', {
            'fields': ('accepts_email_marketing', 'accepts_sms_marketing'),
            'classes': ('collapse',)
        }),
        ('Información Adicional', {
            'fields': ('last_visit_date', 'notes'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_members', 'deactivate_members']
    
    def status_badge(self, obj):
        """Muestra un badge de color según el estado."""
        colors = {
            'active': 'green',
            'inactive': 'gray',
            'suspended': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Estado'
    
    def activate_members(self, request, queryset):
        count = queryset.update(status='active')
        self.message_user(request, f'{count} miembro(s) activado(s).')
    activate_members.short_description = 'Activar miembros seleccionados'
    
    def deactivate_members(self, request, queryset):
        count = queryset.update(status='inactive')
        self.message_user(request, f'{count} miembro(s) desactivado(s).')
    deactivate_members.short_description = 'Desactivar miembros seleccionados'


@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ('member', 'transaction_type', 'points', 'description', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('member__name', 'member__email', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False
