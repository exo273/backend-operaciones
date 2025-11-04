"""
Tests para la aplicación Recipes.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import Recipe, RecipeIngredient
from inventory.models import Category, UnitOfMeasure, Product

User = get_user_model()


class RecipeModelTest(TestCase):
    """Tests para los modelos de Recipes."""

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.unit = UnitOfMeasure.objects.create(name='Gramo', abbreviation='g')
        self.product = Product.objects.create(
            name='Test Ingredient',
            category=self.category,
            inventory_unit=self.unit,
            average_cost=Decimal('10.00')
        )

    def test_create_recipe(self):
        """Test crear una receta."""
        recipe = Recipe.objects.create(
            name='Test Recipe',
            yield_quantity=Decimal('5.000'),
            yield_unit='Porciones'
        )
        self.assertEqual(recipe.name, 'Test Recipe')
        self.assertEqual(recipe.total_cost, Decimal('0.00'))

    def test_recipe_cost_calculation(self):
        """Test cálculo de costo de receta."""
        recipe = Recipe.objects.create(
            name='Recipe with Cost',
            yield_quantity=Decimal('1.000'),
            yield_unit='Unidad'
        )
        ingredient = RecipeIngredient.objects.create(
            recipe=recipe,
            product=self.product,
            quantity_needed=Decimal('100.000'),
            unit='Gramos',
            conversion_factor=Decimal('1.000')
        )
        
        # El costo debería ser 100 * 10 = 1000
        recipe.refresh_from_db()
        self.assertEqual(recipe.total_cost, Decimal('1000.00'))


class RecipeAPITest(TestCase):
    """Tests para la API de Recipes."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name='API Category')
        self.unit = UnitOfMeasure.objects.create(name='Gramo', abbreviation='g')
        self.product = Product.objects.create(
            name='API Ingredient',
            category=self.category,
            inventory_unit=self.unit
        )

    def test_create_recipe_api(self):
        """Test crear receta vía API."""
        data = {
            'name': 'API Recipe',
            'yield_quantity': 10,
            'yield_unit': 'Porciones',
            'ingredients': []
        }
        response = self.client.post(
            '/api/operations/recipes/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_recipes_api(self):
        """Test listar recetas vía API."""
        Recipe.objects.create(
            name='Recipe 1',
            yield_quantity=Decimal('5.000'),
            yield_unit='Unidades'
        )
        response = self.client.get('/api/operations/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
