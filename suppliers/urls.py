"""
URLs para la aplicación Suppliers.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, SupplierCategoryViewSet

router = DefaultRouter()
router.register(r'categories', SupplierCategoryViewSet, basename='supplier-category')
router.register(r'', SupplierViewSet, basename='supplier')

urlpatterns = [
    path('', include(router.urls)),
]
