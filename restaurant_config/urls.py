"""
URLs para configuración del restaurante
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantConfigViewSet

router = DefaultRouter()
router.register(r'', RestaurantConfigViewSet, basename='restaurant-config')

urlpatterns = [
    path('', include(router.urls)),
]
