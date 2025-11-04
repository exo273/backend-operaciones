"""
Views (ViewSets) para la aplicación Suppliers.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Supplier
from .serializers import SupplierSerializer, SupplierListSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de proveedores.
    
    list: Obtener listado de proveedores
    create: Crear nuevo proveedor
    retrieve: Obtener detalle de un proveedor
    update: Actualizar proveedor completo
    partial_update: Actualizar proveedor parcial
    destroy: Eliminar proveedor (soft delete)
    """
    
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'city', 'region']
    search_fields = ['name', 'rut', 'contact_person', 'email']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']

    def get_serializer_class(self):
        """Usar serializer simplificado para listado."""
        if self.action == 'list':
            return SupplierListSerializer
        return SupplierSerializer

    def destroy(self, request, *args, **kwargs):
        """Soft delete: marcar como inactivo en lugar de eliminar."""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Reactivar un proveedor."""
        supplier = self.get_object()
        supplier.is_active = True
        supplier.save()
        serializer = self.get_serializer(supplier)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def purchases(self, request, pk=None):
        """Obtener compras del proveedor."""
        supplier = self.get_object()
        purchases = supplier.purchases.all().order_by('-purchase_date')[:10]
        
        from inventory.serializers import PurchaseListSerializer
        serializer = PurchaseListSerializer(purchases, many=True)
        return Response(serializer.data)
