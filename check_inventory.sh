#!/bin/bash
# Script para verificar el estado del inventario

echo "🔍 Verificando estado del inventario..."
echo ""

echo "📦 Unidades de Medida:"
docker exec backend-operaciones python manage.py shell -c "from inventory.models import UnitOfMeasure; print(f'Total: {UnitOfMeasure.objects.count()}'); [print(f'  - {u.name} ({u.abbreviation})') for u in UnitOfMeasure.objects.all()]"

echo ""
echo "📂 Categorías:"
docker exec backend-operaciones python manage.py shell -c "from inventory.models import Category; print(f'Total: {Category.objects.count()}'); [print(f'  - {c.name}') for c in Category.objects.all()]"

echo ""
echo "📦 Productos:"
docker exec backend-operaciones python manage.py shell -c "from inventory.models import Product; print(f'Total: {Product.objects.count()}'); [print(f'  - {p.name} ({p.category.name}) [{p.inventory_unit.abbreviation}]') for p in Product.objects.all()]"

echo ""
echo "✅ Verificación completada"
