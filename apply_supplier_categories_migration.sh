#!/bin/bash
# Script para aplicar migraciones de categorías de proveedores

echo "🔄 Aplicando migración de categorías de proveedores..."
echo ""

# Aplicar migración
docker exec backend-operaciones python manage.py migrate suppliers

echo ""
echo "✅ Migración completada!"
echo ""
echo "📝 Endpoints disponibles:"
echo "  - GET/POST    /api/operaciones/proveedores/categories/"
echo "  - GET/PUT/PATCH/DELETE /api/operaciones/proveedores/categories/{id}/"
echo "  - GET         /api/operaciones/proveedores/categories/{id}/suppliers/"
echo ""
echo "🎯 Funcionalidades habilitadas:"
echo "  ✅ Crear categorías de proveedores (Carnes, Abarrotes, etc.)"
echo "  ✅ Asignar categoría a cada proveedor"
echo "  ✅ Filtrar proveedores por categoría"
echo "  ✅ Auto-selección de proveedor en compras según categoría del producto"
echo ""
echo "🔗 Próximos pasos:"
echo "  1. Crear categorías de proveedores desde /admin/proveedores"
echo "  2. Asignar categorías a proveedores existentes"
echo "  3. Asignar categorías a productos en /admin/inventario"
echo "  4. Probar auto-selección en /admin/compras"
