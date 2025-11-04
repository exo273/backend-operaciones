"""
URLs para la aplicación Recipes.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, RecipeIngredientViewSet

router = DefaultRouter()
router.register(r'', RecipeViewSet, basename='recipe')
router.register(r'ingredientes', RecipeIngredientViewSet, basename='recipe-ingredient')

urlpatterns = [
    path('', include(router.urls)),
]
