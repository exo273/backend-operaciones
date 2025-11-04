"""
Serializers para la aplicación Inventory.
"""

from rest_framework import serializers
from .models import Category, UnitOfMeasure, Product, PurchaseUnit, Purchase, PurchaseItem
from suppliers.serializers import SupplierListSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para el modelo Category."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    """Serializer para el modelo UnitOfMeasure."""
    
    class Meta:
        model = UnitOfMeasure
        fields = ['id', 'name', 'abbreviation', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PurchaseUnitSerializer(serializers.ModelSerializer):
    """Serializer para el modelo PurchaseUnit."""
    base_unit_name = serializers.CharField(source='base_unit.name', read_only=True)
    base_unit_abbreviation = serializers.CharField(source='base_unit.abbreviation', read_only=True)
    
    class Meta:
        model = PurchaseUnit
        fields = [
            'id',
            'name',
            'base_unit',
            'base_unit_name',
            'base_unit_abbreviation',
            'conversion_factor',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer completo para el modelo Product."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    inventory_unit_name = serializers.CharField(source='inventory_unit.name', read_only=True)
    inventory_unit_abbreviation = serializers.CharField(source='inventory_unit.abbreviation', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'category',
            'category_name',
            'inventory_unit',
            'inventory_unit_name',
            'inventory_unit_abbreviation',
            'current_stock',
            'average_cost',
            'low_stock_threshold',
            'is_low_stock',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'current_stock', 'average_cost', 'created_at', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de productos."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    inventory_unit_abbreviation = serializers.CharField(source='inventory_unit.abbreviation', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category_name',
            'current_stock',
            'inventory_unit_abbreviation',
            'average_cost',
            'is_low_stock',
            'is_active',
        ]


class PurchaseItemSerializer(serializers.ModelSerializer):
    """Serializer para el modelo PurchaseItem."""
    product_name = serializers.CharField(source='product.name', read_only=True)
    purchase_unit_name = serializers.CharField(source='purchase_unit.name', read_only=True)
    
    class Meta:
        model = PurchaseItem
        fields = [
            'id',
            'purchase',
            'product',
            'product_name',
            'quantity_purchased',
            'purchase_unit',
            'purchase_unit_name',
            'total_cost',
            'calculated_net_cost_per_base_unit',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'calculated_net_cost_per_base_unit', 'created_at', 'updated_at']


class PurchaseSerializer(serializers.ModelSerializer):
    """Serializer completo para el modelo Purchase."""
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    items = PurchaseItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Purchase
        fields = [
            'id',
            'supplier',
            'supplier_name',
            'purchase_date',
            'document_type',
            'document_number',
            'notes',
            'total_amount',
            'items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']


class PurchaseListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de compras."""
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    items_count = serializers.IntegerField(source='items.count', read_only=True)
    
    class Meta:
        model = Purchase
        fields = [
            'id',
            'supplier_name',
            'purchase_date',
            'document_type',
            'document_number',
            'total_amount',
            'items_count',
        ]


class PurchaseCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear una compra con sus ítems."""
    items = PurchaseItemSerializer(many=True)
    
    class Meta:
        model = Purchase
        fields = [
            'id',
            'supplier',
            'purchase_date',
            'document_type',
            'document_number',
            'notes',
            'items',
        ]

    def create(self, validated_data):
        """Crear compra con sus ítems."""
        items_data = validated_data.pop('items')
        purchase = Purchase.objects.create(**validated_data)
        
        for item_data in items_data:
            PurchaseItem.objects.create(purchase=purchase, **item_data)
        
        # Calcular el total
        purchase.calculate_total()
        
        return purchase
