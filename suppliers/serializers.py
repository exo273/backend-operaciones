"""
Serializers para la aplicación Suppliers.
"""

from rest_framework import serializers
from .models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Supplier."""
    
    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
            'rut',
            'contact_person',
            'phone',
            'email',
            'address',
            'city',
            'region',
            'website',
            'notes',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_rut(self, value):
        """Validación adicional del RUT."""
        # El modelo ya valida el formato y dígito verificador
        return value


class SupplierListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de proveedores."""
    
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'rut', 'contact_person', 'phone', 'email', 'is_active']
