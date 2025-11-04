# Ejemplos de Uso de la API - Backend Operaciones

Este documento contiene ejemplos prácticos de cómo usar la API REST del servicio de operaciones.

## Configuración Inicial

Todas las peticiones requieren autenticación JWT. Primero obtén un token:

```powershell
# PowerShell
$response = Invoke-RestMethod -Uri "http://localhost:8001/api/token/" `
    -Method Post `
    -Body (@{username="admin";password="admin123"} | ConvertTo-Json) `
    -ContentType "application/json"

$token = $response.access
$headers = @{Authorization="Bearer $token"}
```

## 1. Proveedores

### Crear un proveedor

```powershell
$body = @{
    name = "Distribuidora Central S.A."
    rut = "76543210-9"
    contact_person = "María González"
    phone = "+56987654321"
    email = "contacto@distribuidora.cl"
    address = "Av. Industrial 456"
    city = "Santiago"
    region = "Región Metropolitana"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/api/operations/suppliers/" `
    -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

### Listar proveedores activos

```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/suppliers/?is_active=true" `
    -Headers $headers
```

### Buscar proveedor por nombre

```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/suppliers/?search=Distribuidora" `
    -Headers $headers
```

## 2. Inventario

### Crear una categoría

```powershell
$body = @{
    name = "Carnes"
    description = "Carnes rojas, blancas y embutidos"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/categories/" `
    -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

### Crear unidad de medida

```powershell
$body = @{
    name = "Kilogramo"
    abbreviation = "kg"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/units/" `
    -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

### Crear unidad de compra

```powershell
$body = @{
    name = "Saco 25kg"
    base_unit = 1  # ID de la unidad base (ej: gramos)
    conversion_factor = 25000
    description = "Saco de 25 kilogramos"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/purchase-units/" `
    -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

### Crear un producto

```powershell
$body = @{
    name = "Carne de Res Molida"
    description = "Carne de res molida premium"
    category = 1  # ID de categoría Carnes
    inventory_unit = 1  # ID de unidad (gramos)
    low_stock_threshold = 5000  # 5kg
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/" `
    -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

### Listar productos con stock bajo

```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/low_stock/" `
    -Headers $headers
```

### Ver historial de stock de un producto

```powershell
$productId = 1
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/$productId/stock_history/" `
    -Headers $headers
```

## 3. Compras

### Registrar una compra con ítems

```powershell
$body = @{
    supplier = 1  # ID del proveedor
    purchase_date = "2025-10-30"
    document_type = "FACTURA"
    document_number = "F-12345"
    notes = "Compra mensual de productos"
    items = @(
        @{
            product = 1  # ID del producto
            quantity_purchased = 2
            purchase_unit = 1  # ID de unidad de compra (ej: Saco 25kg)
            total_cost = 95000
            notes = "Producto en buen estado"
        },
        @{
            product = 2
            quantity_purchased = 5
            purchase_unit = 2
            total_cost = 45000
        }
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/purchases/" `
    -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

### Listar compras

```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/purchases/" `
    -Headers $headers
```

### Filtrar compras por proveedor

```powershell
$supplierId = 1
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/purchases/?supplier=$supplierId" `
    -Headers $headers
```

### Filtrar compras por fecha

```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/purchases/?purchase_date=2025-10-30" `
    -Headers $headers
```

### Agregar ítem a una compra existente

```powershell
$purchaseId = 1
$body = @{
    product = 3
    quantity_purchased = 1
    purchase_unit = 3
    total_cost = 25000
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/purchases/$purchaseId/add_item/" `
    -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

## 4. Recetas

### Crear una receta con ingredientes

```powershell
$body = @{
    name = "Hamburguesa Premium"
    description = "Hamburguesa gourmet con carne de res"
    instructions = "1. Mezclar ingredientes. 2. Formar hamburguesas. 3. Cocinar."
    yield_quantity = 10
    yield_unit = "Unidades"
    preparation_time = 30
    is_active = $true
    ingredients = @(
        @{
            product = 1  # Carne molida
            quantity_needed = 1500  # 1.5kg
            unit = "Gramos"
            conversion_factor = 1  # 1:1 porque ya está en gramos
            notes = "Carne de primera calidad"
        },
        @{
            product = 4  # Pan de hamburguesa
            quantity_needed = 10
            unit = "Unidades"
            conversion_factor = 1
        },
        @{
            product = 5  # Queso
            quantity_needed = 500
            unit = "Gramos"
            conversion_factor = 1
        }
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8001/api/operations/recipes/" `
    -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

### Listar recetas activas

```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/recipes/?is_active=true" `
    -Headers $headers
```

### Ver desglose de costos de una receta

```powershell
$recipeId = 1
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/recipes/$recipeId/cost_breakdown/" `
    -Headers $headers
```

### Recalcular costo de una receta

```powershell
$recipeId = 1
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/recipes/$recipeId/recalculate_cost/" `
    -Method Post -Headers $headers
```

### Agregar ingrediente a receta existente

```powershell
$recipeId = 1
$body = @{
    product = 6  # Nuevo producto
    quantity_needed = 200
    unit = "Gramos"
    conversion_factor = 1
    notes = "Opcional"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/api/operations/recipes/$recipeId/add_ingredient/" `
    -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

## 5. Búsquedas y Filtros

### Buscar productos por nombre

```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/?search=carne" `
    -Headers $headers
```

### Filtrar productos por categoría

```powershell
$categoryId = 1
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/?category=$categoryId" `
    -Headers $headers
```

### Ordenar productos por stock

```powershell
# Ascendente
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/?ordering=current_stock" `
    -Headers $headers

# Descendente
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/?ordering=-current_stock" `
    -Headers $headers
```

### Paginación

```powershell
# Primera página
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/?page=1" `
    -Headers $headers

# Segunda página
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/?page=2" `
    -Headers $headers
```

## 6. Actualización y Eliminación

### Actualizar un producto (PUT - completo)

```powershell
$productId = 1
$body = @{
    name = "Carne de Res Molida Premium"
    description = "Carne de res molida de primera calidad"
    category = 1
    inventory_unit = 1
    low_stock_threshold = 10000
    is_active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/$productId/" `
    -Method Put -Headers $headers -Body $body -ContentType "application/json"
```

### Actualizar parcialmente (PATCH)

```powershell
$productId = 1
$body = @{
    low_stock_threshold = 8000
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/$productId/" `
    -Method Patch -Headers $headers -Body $body -ContentType "application/json"
```

### Desactivar un proveedor (soft delete)

```powershell
$supplierId = 1
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/suppliers/$supplierId/" `
    -Method Delete -Headers $headers
```

### Reactivar un proveedor

```powershell
$supplierId = 1
Invoke-RestMethod -Uri "http://localhost:8001/api/operations/suppliers/$supplierId/activate/" `
    -Method Post -Headers $headers
```

## 7. Ejemplos con cURL (alternativa)

### Obtener token

```bash
curl -X POST http://localhost:8001/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Listar productos

```bash
TOKEN="tu-token-aqui"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8001/api/operations/inventory/products/
```

### Crear producto

```bash
TOKEN="tu-token-aqui"
curl -X POST http://localhost:8001/api/operations/inventory/products/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Producto Nuevo",
    "category": 1,
    "inventory_unit": 1
  }'
```

## 8. Manejo de Errores

### Error 401 - No autenticado

```powershell
# Respuesta:
@{
    detail = "Las credenciales de autenticación no se proveyeron."
}
```

### Error 400 - Validación

```powershell
# Respuesta:
@{
    name = @("Este campo es requerido.")
    rut = @("RUT debe estar en formato 12345678-9 o 12345678-K")
}
```

### Error 404 - No encontrado

```powershell
# Respuesta:
@{
    detail = "No encontrado."
}
```

## 9. Tips y Mejores Prácticas

1. **Siempre validar el token**: Los tokens JWT expiran. Usa el refresh token si es necesario.

2. **Usar filtros**: Aprovecha los query parameters para filtrar y reducir la cantidad de datos.

3. **Paginación**: Para listas grandes, usa paginación para mejorar el rendimiento.

4. **Ordenamiento**: Ordena los resultados según tus necesidades con el parámetro `ordering`.

5. **Búsqueda**: Usa el parámetro `search` para búsquedas de texto completo.

6. **Manejo de errores**: Siempre verifica el código de estado HTTP y maneja los errores apropiadamente.

7. **Soft delete**: Los proveedores usan soft delete (is_active=false), no se eliminan físicamente.

## 10. Flujo Completo de Ejemplo

```powershell
# 1. Autenticarse
$token = (Invoke-RestMethod -Uri "http://localhost:8001/api/token/" -Method Post -Body (@{username="admin";password="admin123"} | ConvertTo-Json) -ContentType "application/json").access
$headers = @{Authorization="Bearer $token"}

# 2. Crear categoría
$category = Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/categories/" -Method Post -Headers $headers -Body (@{name="Carnes";description="Productos cárnicos"} | ConvertTo-Json) -ContentType "application/json"

# 3. Crear unidad de medida
$unit = Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/units/" -Method Post -Headers $headers -Body (@{name="Gramo";abbreviation="g"} | ConvertTo-Json) -ContentType "application/json"

# 4. Crear producto
$product = Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/" -Method Post -Headers $headers -Body (@{name="Carne Molida";category=$category.id;inventory_unit=$unit.id} | ConvertTo-Json) -ContentType "application/json"

# 5. Crear proveedor
$supplier = Invoke-RestMethod -Uri "http://localhost:8001/api/operations/suppliers/" -Method Post -Headers $headers -Body (@{name="Proveedor Test";rut="12345678-9";email="test@test.cl"} | ConvertTo-Json) -ContentType "application/json"

# 6. Registrar compra
$purchase = Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/purchases/" -Method Post -Headers $headers -Body (@{supplier=$supplier.id;purchase_date="2025-10-30";document_type="FACTURA";document_number="F-001";items=@(@{product=$product.id;quantity_purchased=10;purchase_unit=1;total_cost=50000})} | ConvertTo-Json -Depth 3) -ContentType "application/json"

# 7. Ver producto actualizado con stock
$updatedProduct = Invoke-RestMethod -Uri "http://localhost:8001/api/operations/inventory/products/$($product.id)/" -Headers $headers

Write-Host "Stock actual: $($updatedProduct.current_stock)"
Write-Host "Costo promedio: $($updatedProduct.average_cost)"
```
