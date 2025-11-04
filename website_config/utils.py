"""
Utilidades para el módulo de configuración web.
"""
from inventory.models import Product, Category


def get_public_menu_data():
    """
    Obtiene el menú completo en formato JSON para la página web pública
    y para la señalización digital.
    
    Returns:
        dict: Diccionario con categorías y productos activos en la web
    """
    # Obtener productos activos para web ordenados por categoría y orden
    products = Product.objects.filter(
        is_active_website=True
    ).select_related('category').order_by('category__display_order', 'category__name', 'name')
    
    # Obtener categorías activas con productos
    active_category_ids = products.values_list('category_id', flat=True).distinct()
    categories = Category.objects.filter(
        id__in=active_category_ids
    ).order_by('display_order', 'name')
    
    # Construir estructura de datos
    categories_data = []
    for category in categories:
        categories_data.append({
            'id': category.id,
            'name': category.name,
            'description': category.description or '',
        })
    
    products_data = []
    for product in products:
        # Determinar precio y descripción para mostrar
        web_price = product.web_price if product.web_price else product.price
        description_display = product.web_description if product.web_description else product.description
        
        products_data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description or '',
            'description_display': description_display or '',
            'category_id': product.category_id,
            'category_name': product.category.name,
            'price': str(product.price),
            'web_price': str(web_price),
            'has_web_image': bool(product.web_image),
            'web_image_url': product.web_image.url if product.web_image else None,
            'allergens': product.allergens or '',
            'is_featured': product.is_featured,
        })
    
    return {
        'categories': categories_data,
        'products': products_data,
    }
