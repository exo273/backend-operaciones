#!/bin/bash
# Script para crear unidades de medida básicas en el contenedor

echo "🔧 Creando unidades de medida básicas..."
echo ""

docker exec backend-operaciones python manage.py shell < create_units.py

echo ""
echo "✅ Proceso completado!"
echo ""
echo "📋 Ahora puedes:"
echo "  1. Recargar la página de Inventario"
echo "  2. Hacer clic en 'Nuevo Producto'"
echo "  3. Ver las unidades de medida disponibles"
