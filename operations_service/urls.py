"""
URL Configuration for operations_service project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints - Internal (requieren autenticación)
    path('api/operations/suppliers/', include('suppliers.urls')),
    path('api/operations/inventory/', include('inventory.urls')),
    path('api/operations/recipes/', include('recipes.urls')),
    
    # API endpoints - Public (sin autenticación para el sitio web)
    path('api/website/', include('website_api_urls')),
]
