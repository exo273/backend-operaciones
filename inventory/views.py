"""
Views (ViewSets) para la aplicación Inventory.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, UnitOfMeasure, Product, PurchaseUnit, Purchase, PurchaseItem
from .serializers import (
    CategorySerializer,
    UnitOfMeasureSerializer,
    ProductSerializer,
    ProductListSerializer,
    PurchaseUnitSerializer,
    PurchaseSerializer,
    PurchaseListSerializer,
    PurchaseCreateSerializer,
    PurchaseItemSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de categorías."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de unidades de medida."""
    
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'abbreviation']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class PurchaseUnitViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de unidades de compra."""
    
    queryset = PurchaseUnit.objects.all()
    serializer_class = PurchaseUnitSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['base_unit']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de productos."""
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'inventory_unit', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'current_stock', 'average_cost', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        """Usar serializer simplificado para listado."""
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Obtener productos con stock bajo."""
        low_stock_products = [p for p in self.get_queryset() if p.is_low_stock]
        serializer = ProductListSerializer(low_stock_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stock_history(self, request, pk=None):
        """Obtener historial de movimientos de stock del producto."""
        product = self.get_object()
        
        # Obtener compras del producto
        purchases = product.purchase_items.all().order_by('-created_at')[:20]
        purchase_serializer = PurchaseItemSerializer(purchases, many=True)
        
        return Response({
            'product_id': product.id,
            'product_name': product.name,
            'current_stock': product.current_stock,
            'average_cost': product.average_cost,
            'purchases': purchase_serializer.data,
        })


class PurchaseViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de compras."""
    
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['supplier', 'document_type', 'purchase_date']
    search_fields = ['document_number', 'supplier__name', 'notes']
    ordering_fields = ['purchase_date', 'total_amount', 'created_at']
    ordering = ['-purchase_date']

    def get_serializer_class(self):
        """Usar serializers específicos según la acción."""
        if self.action == 'list':
            return PurchaseListSerializer
        elif self.action == 'create':
            return PurchaseCreateSerializer
        return PurchaseSerializer

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Agregar un ítem a una compra existente."""
        purchase = self.get_object()
        serializer = PurchaseItemSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(purchase=purchase)
            purchase.calculate_total()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseItemViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de ítems de compra."""
    
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['purchase', 'product']
    search_fields = ['product__name', 'notes']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
