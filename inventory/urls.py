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
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'units', UnitOfMeasureViewSet, basename='unit')
router.register(r'purchase-units', PurchaseUnitViewSet, basename='purchase-unit')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'purchases', PurchaseViewSet, basename='purchase')
router.register(r'purchase-items', PurchaseItemViewSet, basename='purchase-item')

urlpatterns = [
    path('', include(router.urls)),
]
