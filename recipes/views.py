"""
Views (ViewSets) para la aplicación Recipes.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe, RecipeIngredient
from .serializers import (
    RecipeSerializer,
    RecipeListSerializer,
    RecipeCreateSerializer,
    RecipeIngredientSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de recetas."""
    
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'yield_unit']
    search_fields = ['name', 'description', 'instructions']
    ordering_fields = ['name', 'total_cost', 'cost_per_unit', 'preparation_time', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        """Usar serializers específicos según la acción."""
        if self.action == 'list':
            return RecipeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(detail=True, methods=['post'])
    def recalculate_cost(self, request, pk=None):
        """Recalcular el costo de una receta."""
        recipe = self.get_object()
        new_cost = recipe.calculate_cost()
        
        serializer = self.get_serializer(recipe)
        return Response({
            'message': 'Costo recalculado exitosamente',
            'recipe': serializer.data,
            'new_total_cost': new_cost,
        })

    @action(detail=True, methods=['post'])
    def add_ingredient(self, request, pk=None):
        """Agregar un ingrediente a una receta existente."""
        recipe = self.get_object()
        serializer = RecipeIngredientSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def cost_breakdown(self, request, pk=None):
        """Obtener desglose detallado de costos de la receta."""
        recipe = self.get_object()
        ingredients = recipe.ingredients.all()
        
        breakdown = []
        for ingredient in ingredients:
            breakdown.append({
                'product_name': ingredient.product.name,
                'quantity_needed': ingredient.quantity_needed,
                'unit': ingredient.unit,
                'conversion_factor': ingredient.conversion_factor,
                'product_average_cost': ingredient.product.average_cost,
                'calculated_cost': ingredient.calculated_cost,
                'percentage_of_total': (ingredient.calculated_cost / recipe.total_cost * 100) if recipe.total_cost > 0 else 0,
            })
        
        return Response({
            'recipe_name': recipe.name,
            'total_cost': recipe.total_cost,
            'cost_per_unit': recipe.cost_per_unit,
            'yield_quantity': recipe.yield_quantity,
            'yield_unit': recipe.yield_unit,
            'ingredients_breakdown': breakdown,
        })


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de ingredientes de recetas."""
    
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['recipe', 'product']
    search_fields = ['product__name', 'notes']
    ordering_fields = ['created_at']
    ordering = ['recipe', 'product']

    def perform_update(self, serializer):
        """Al actualizar, recalcular costos."""
        serializer.save()
        # El modelo ya se encarga de recalcular los costos

    def perform_destroy(self, instance):
        """Al eliminar, recalcular costos de la receta."""
        instance.delete()
        # El modelo ya se encarga de recalcular los costos
