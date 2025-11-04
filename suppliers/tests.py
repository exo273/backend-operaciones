"""
Tests para la aplicación Suppliers.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Supplier

User = get_user_model()


class SupplierModelTest(TestCase):
    """Tests para el modelo Supplier."""

    def setUp(self):
        self.supplier_data = {
            'name': 'Test Supplier',
            'rut': '12345678-9',
            'contact_person': 'John Doe',
            'phone': '+56912345678',
            'email': 'test@test.com',
        }

    def test_create_supplier(self):
        """Test crear un proveedor."""
        supplier = Supplier.objects.create(**self.supplier_data)
        self.assertEqual(supplier.name, 'Test Supplier')
        self.assertTrue(supplier.is_active)

    def test_supplier_str(self):
        """Test representación string del proveedor."""
        supplier = Supplier.objects.create(**self.supplier_data)
        self.assertEqual(str(supplier), 'Test Supplier (12345678-9)')


class SupplierAPITest(TestCase):
    """Tests para la API de proveedores."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.supplier_data = {
            'name': 'API Test Supplier',
            'rut': '87654321-0',
            'email': 'api@test.com',
        }

    def test_create_supplier_api(self):
        """Test crear proveedor vía API."""
        response = self.client.post(
            '/api/operations/suppliers/',
            self.supplier_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 1)

    def test_list_suppliers_api(self):
        """Test listar proveedores vía API."""
        Supplier.objects.create(**self.supplier_data)
        response = self.client.get('/api/operations/suppliers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
