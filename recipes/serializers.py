"""
Serializers para la aplicación Recipes.
"""

from rest_framework import serializers
from .models import Recipe, RecipeIngredient
from inventory.serializers import ProductListSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Serializer para el modelo RecipeIngredient."""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_unit_abbreviation = serializers.CharField(source='product.inventory_unit.abbreviation', read_only=True)
    product_average_cost = serializers.DecimalField(source='product.average_cost', read_only=True, max_digits=12, decimal_places=2)
    
    class Meta:
        model = RecipeIngredient
        fields = [
            'id',
            'recipe',
            'product',
            'product_name',
            'product_unit_abbreviation',
            'product_average_cost',
            'quantity_needed',
            'unit',
            'conversion_factor',
            'notes',
            'calculated_cost',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'calculated_cost', 'created_at', 'updated_at']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer completo para el modelo Recipe."""
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    ingredients_count = serializers.IntegerField(source='ingredients.count', read_only=True)
    
    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'description',
            'instructions',
            'yield_quantity',
            'yield_unit',
            'total_cost',
            'cost_per_unit',
            'preparation_time',
            'is_active',
            'ingredients',
            'ingredients_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'total_cost', 'cost_per_unit', 'created_at', 'updated_at']


class RecipeListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de recetas."""
    ingredients_count = serializers.IntegerField(source='ingredients.count', read_only=True)
    
    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'yield_quantity',
            'yield_unit',
            'total_cost',
            'cost_per_unit',
            'ingredients_count',
            'is_active',
        ]


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear una receta con sus ingredientes."""
    ingredients = RecipeIngredientSerializer(many=True)
    
    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'description',
            'instructions',
            'yield_quantity',
            'yield_unit',
            'preparation_time',
            'is_active',
            'ingredients',
        ]

    def create(self, validated_data):
        """Crear receta con sus ingredientes."""
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient_data)
        
        # El cálculo de costos se hace automáticamente en el modelo
        return recipe

    def update(self, instance, validated_data):
        """Actualizar receta y sus ingredientes."""
        ingredients_data = validated_data.pop('ingredients', None)
        
        # Actualizar campos de la receta
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Si se proporcionaron ingredientes, actualizarlos
        if ingredients_data is not None:
            # Eliminar ingredientes existentes
            instance.ingredients.all().delete()
            
            # Crear nuevos ingredientes
            for ingredient_data in ingredients_data:
                RecipeIngredient.objects.create(recipe=instance, **ingredient_data)
        
        return instance
