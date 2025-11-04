"""
Script para inicializar datos básicos del sistema.
Ejecutar con: python manage.py shell < scripts/init_data.py
"""

from django.db import transaction
from inventory.models import Category, UnitOfMeasure, PurchaseUnit
from suppliers.models import Supplier

print("Inicializando datos básicos del sistema...")

with transaction.atomic():
    # Crear Categorías
    print("\n1. Creando categorías...")
    categories_data = [
        {"name": "Lácteos", "description": "Productos lácteos y derivados"},
        {"name": "Carnes", "description": "Carnes rojas, blancas y embutidos"},
        {"name": "Verduras", "description": "Verduras y hortalizas frescas"},
        {"name": "Frutas", "description": "Frutas frescas y congeladas"},
        {"name": "Abarrotes", "description": "Productos secos y no perecederos"},
        {"name": "Condimentos", "description": "Especias, hierbas y condimentos"},
        {"name": "Bebidas", "description": "Bebidas y líquidos"},
        {"name": "Panadería", "description": "Pan, masas y productos de panadería"},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"description": cat_data["description"]}
        )
        if created:
            print(f"  ✓ Categoría creada: {category.name}")
        else:
            print(f"  - Categoría ya existe: {category.name}")

    # Crear Unidades de Medida Base
    print("\n2. Creando unidades de medida base...")
    units_data = [
        {"name": "Gramo", "abbreviation": "g"},
        {"name": "Kilogramo", "abbreviation": "kg"},
        {"name": "Litro", "abbreviation": "L"},
        {"name": "Mililitro", "abbreviation": "ml"},
        {"name": "Unidad", "abbreviation": "un"},
    ]
    
    for unit_data in units_data:
        unit, created = UnitOfMeasure.objects.get_or_create(
            abbreviation=unit_data["abbreviation"],
            defaults={"name": unit_data["name"]}
        )
        if created:
            print(f"  ✓ Unidad creada: {unit.name} ({unit.abbreviation})")
        else:
            print(f"  - Unidad ya existe: {unit.name} ({unit.abbreviation})")

    # Crear Unidades de Compra comunes
    print("\n3. Creando unidades de compra...")
    
    # Obtener unidades base
    gramo = UnitOfMeasure.objects.get(abbreviation="g")
    litro = UnitOfMeasure.objects.get(abbreviation="L")
    unidad = UnitOfMeasure.objects.get(abbreviation="un")
    
    purchase_units_data = [
        {"name": "Saco 25kg", "base_unit": gramo, "conversion_factor": 25000},
        {"name": "Saco 50kg", "base_unit": gramo, "conversion_factor": 50000},
        {"name": "Caja 10kg", "base_unit": gramo, "conversion_factor": 10000},
        {"name": "Bolsa 1kg", "base_unit": gramo, "conversion_factor": 1000},
        {"name": "Bidón 5L", "base_unit": litro, "conversion_factor": 5},
        {"name": "Bidón 20L", "base_unit": litro, "conversion_factor": 20},
        {"name": "Botella 1L", "base_unit": litro, "conversion_factor": 1},
        {"name": "Caja 12 unidades", "base_unit": unidad, "conversion_factor": 12},
        {"name": "Caja 24 unidades", "base_unit": unidad, "conversion_factor": 24},
    ]
    
    for pu_data in purchase_units_data:
        purchase_unit, created = PurchaseUnit.objects.get_or_create(
            name=pu_data["name"],
            defaults={
                "base_unit": pu_data["base_unit"],
                "conversion_factor": pu_data["conversion_factor"]
            }
        )
        if created:
            print(f"  ✓ Unidad de compra creada: {purchase_unit.name}")
        else:
            print(f"  - Unidad de compra ya existe: {purchase_unit.name}")

    # Crear un proveedor de ejemplo
    print("\n4. Creando proveedor de ejemplo...")
    supplier, created = Supplier.objects.get_or_create(
        rut="12345678-9",
        defaults={
            "name": "Distribuidora Ejemplo S.A.",
            "contact_person": "Juan Pérez",
            "phone": "+56912345678",
            "email": "contacto@ejemplo.cl",
            "address": "Av. Principal 123",
            "city": "Santiago",
            "region": "Región Metropolitana",
        }
    )
    if created:
        print(f"  ✓ Proveedor creado: {supplier.name}")
    else:
        print(f"  - Proveedor ya existe: {supplier.name}")

print("\n✅ Datos básicos inicializados correctamente!")
print("\nPróximos pasos:")
print("1. Crear productos en /admin/ o vía API")
print("2. Registrar compras para actualizar stock")
print("3. Crear recetas con los productos")
