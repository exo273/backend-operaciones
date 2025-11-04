"""
URLs para la aplicación Inventory.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    UnitOfMeasureViewSet,
    PurchaseUnitViewSet,
    ProductViewSet,
    PurchaseViewSet,
    PurchaseItemViewSet,
)

router = DefaultRouter()
router.register(r'categorias', CategoryViewSet, basename='category')
router.register(r'unidades', UnitOfMeasureViewSet, basename='unit')
router.register(r'unidades-compra', PurchaseUnitViewSet, basename='purchase-unit')
router.register(r'productos', ProductViewSet, basename='product')
router.register(r'compras', PurchaseViewSet, basename='purchase')
router.register(r'items-compra', PurchaseItemViewSet, basename='purchase-item')

urlpatterns = [
    path('', include(router.urls)),
]
