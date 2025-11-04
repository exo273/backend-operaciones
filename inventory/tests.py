"""
Tests para la aplicación Inventory.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import Category, UnitOfMeasure, Product, PurchaseUnit
from suppliers.models import Supplier

User = get_user_model()


class InventoryModelTest(TestCase):
    """Tests para los modelos de Inventory."""

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.unit = UnitOfMeasure.objects.create(name='Gramo', abbreviation='g')

    def test_create_product(self):
        """Test crear un producto."""
        product = Product.objects.create(
            name='Test Product',
            category=self.category,
            inventory_unit=self.unit,
            current_stock=Decimal('100.000'),
            average_cost=Decimal('10.00')
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.current_stock, Decimal('100.000'))

    def test_product_low_stock(self):
        """Test detección de stock bajo."""
        product = Product.objects.create(
            name='Low Stock Product',
            category=self.category,
            inventory_unit=self.unit,
            current_stock=Decimal('5.000'),
            low_stock_threshold=Decimal('10.000')
        )
        self.assertTrue(product.is_low_stock)


class InventoryAPITest(TestCase):
    """Tests para la API de Inventory."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name='API Category')
        self.unit = UnitOfMeasure.objects.create(name='Kilogramo', abbreviation='kg')

    def test_create_product_api(self):
        """Test crear producto vía API."""
        data = {
            'name': 'API Product',
            'category': self.category.id,
            'inventory_unit': self.unit.id,
        }
        response = self.client.post(
            '/api/operations/inventory/products/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_products_api(self):
        """Test listar productos vía API."""
        Product.objects.create(
            name='Product 1',
            category=self.category,
            inventory_unit=self.unit
        )
        response = self.client.get('/api/operations/inventory/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
