"""
Serializers para la aplicación Suppliers.
"""

from rest_framework import serializers
from .models import Supplier, SupplierCategory


class SupplierCategorySerializer(serializers.ModelSerializer):
    """Serializer para el modelo SupplierCategory."""
    
    suppliers_count = serializers.IntegerField(
        source='suppliers.count',
        read_only=True
    )
    
    class Meta:
        model = SupplierCategory
        fields = [
            'id',
            'name',
            'description',
            'suppliers_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'suppliers_count']


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Supplier."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
            'rut',
            'category',
            'category_name',
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
        read_only_fields = ['id', 'created_at', 'updated_at', 'category_name']

    def validate_rut(self, value):
        """Validación adicional del RUT."""
        # El modelo ya valida el formato y dígito verificador
        return value


class SupplierListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de proveedores."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'rut', 'category', 'category_name', 'contact_person', 'phone', 'email', 'is_active']
