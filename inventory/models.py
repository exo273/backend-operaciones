"""
Modelos de la aplicación Inventory.
Gestiona categorías, unidades de medida, productos, compras y stock.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db import transaction


class Category(models.Model):
    """Categoría de productos."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name


class UnitOfMeasure(models.Model):
    """Unidad de medida base (para inventario)."""
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    abbreviation = models.CharField(max_length=10, unique=True, verbose_name="Abreviación")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class Product(models.Model):
    """Producto en inventario."""
    name = models.CharField(max_length=200, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Categoría"
    )
    inventory_unit = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Unidad de Inventario",
        help_text="Unidad base en la que se maneja el stock"
    )
    current_stock = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Stock Actual"
    )
    average_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Costo Promedio",
        help_text="Costo promedio por unidad de inventario"
    )
    low_stock_threshold = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Umbral de Stock Bajo",
        help_text="Alerta cuando el stock sea menor a este valor"
    )
    waste_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))],
        verbose_name="Porcentaje de Merma",
        help_text="Porcentaje de merma o desperdicio del producto (0-100%)"
    )
    
    # Campos para el sitio web
    is_active_pos = models.BooleanField(
        default=True,
        verbose_name="Activo en POS",
        help_text="Mostrar en el sistema de punto de venta"
    )
    is_active_website = models.BooleanField(
        default=False,
        verbose_name="Activo en Web",
        help_text="Mostrar en el menú de la página web"
    )
    description_web = models.TextField(
        blank=True,
        verbose_name="Descripción para Web",
        help_text="Descripción atractiva para el sitio web (deja vacío para usar la descripción normal)"
    )
    image = models.ImageField(
        upload_to='products/images/',
        blank=True,
        null=True,
        verbose_name="Imagen del Producto",
        help_text="Imagen para mostrar en la web"
    )
    web_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Precio Web",
        help_text="Precio mostrado en la web (opcional)"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden de Visualización",
        help_text="Orden en el menú web (menor primero)"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['name']
        indexes = [
            models.Index(fields=['category', 'name']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.inventory_unit.abbreviation})"

    @property
    def is_low_stock(self):
        """Indica si el producto tiene stock bajo."""
        if self.low_stock_threshold is not None:
            return self.current_stock <= self.low_stock_threshold
        return False
    
    def get_web_description(self):
        """Retorna la descripción para la web o la descripción normal."""
        return self.description_web if self.description_web else self.description
    
    def get_image_url(self):
        """Retorna la URL de la imagen si existe."""
        if self.image:
            return self.image.url
        return None

    def update_stock_and_cost(self, quantity_change, new_item_cost=None, new_quantity_in_base=None):
        """
        Actualiza el stock y recalcula el costo promedio.
        
        Args:
            quantity_change: Cambio en la cantidad (positivo para compra, negativo para venta)
            new_item_cost: Costo total del nuevo ítem (para compras)
            new_quantity_in_base: Cantidad en unidades base del nuevo ítem
        """
        with transaction.atomic():
            if quantity_change > 0 and new_item_cost is not None and new_quantity_in_base is not None:
                # Compra: recalcular costo promedio ponderado
                current_total_value = self.current_stock * self.average_cost
                new_total_value = current_total_value + new_item_cost
                new_total_stock = self.current_stock + new_quantity_in_base
                
                if new_total_stock > 0:
                    self.average_cost = new_total_value / new_total_stock
            
            # Actualizar stock
            self.current_stock += quantity_change
            if self.current_stock < 0:
                self.current_stock = Decimal('0')
            
            self.save()


class PurchaseUnit(models.Model):
    """Unidad de compra (puede ser diferente a la unidad de inventario)."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    base_unit = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        related_name='purchase_units',
        verbose_name="Unidad Base"
    )
    conversion_factor = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Factor de Conversión",
        help_text="Cantidad de unidades base en esta unidad de compra (ej: 25000 para un saco de 25kg)"
    )
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Unidad de Compra"
        verbose_name_plural = "Unidades de Compra"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} = {self.conversion_factor} {self.base_unit.abbreviation}"


class Purchase(models.Model):
    """Orden de compra a proveedor."""
    DOCUMENT_TYPES = [
        ('FACTURA', 'Factura'),
        ('BOLETA', 'Boleta'),
        ('GUIA', 'Guía de Despacho'),
    ]

    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.PROTECT,
        related_name='purchases',
        verbose_name="Proveedor"
    )
    purchase_date = models.DateField(verbose_name="Fecha de Compra")
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES,
        verbose_name="Tipo de Documento"
    )
    document_number = models.CharField(max_length=50, verbose_name="Número de Documento")
    notes = models.TextField(blank=True, verbose_name="Notas")
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Monto Total"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-purchase_date', '-created_at']
        unique_together = [['document_type', 'document_number']]
        indexes = [
            models.Index(fields=['supplier', '-purchase_date']),
            models.Index(fields=['-purchase_date']),
        ]

    def __str__(self):
        return f"{self.document_type} {self.document_number} - {self.supplier.name}"

    def calculate_total(self):
        """Calcula el total de la compra sumando los ítems."""
        total = sum(item.total_cost for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])
        return total


class PurchaseItem(models.Model):
    """Ítem individual en una compra."""
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Compra"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='purchase_items',
        verbose_name="Producto"
    )
    quantity_purchased = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Cantidad Comprada"
    )
    purchase_unit = models.ForeignKey(
        PurchaseUnit,
        on_delete=models.PROTECT,
        related_name='purchase_items',
        verbose_name="Unidad de Compra"
    )
    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Costo Total del Ítem",
        help_text="Costo total con IVA incluido"
    )
    calculated_net_cost_per_base_unit = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=Decimal('0.0000'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Costo Neto por Unidad Base",
        help_text="Calculado automáticamente al guardar"
    )
    notes = models.TextField(blank=True, verbose_name="Notas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ítem de Compra"
        verbose_name_plural = "Ítems de Compra"
        ordering = ['purchase', 'product']

    def __str__(self):
        return f"{self.product.name} - {self.quantity_purchased} {self.purchase_unit.name}"

    def save(self, *args, **kwargs):
        """
        Al guardar, calcula el costo neto por unidad base y actualiza el stock del producto.
        """
        is_new = self.pk is None
        
        # Calcular cantidad en unidades base
        quantity_in_base_units = self.quantity_purchased * self.purchase_unit.conversion_factor
        
        # Calcular costo neto (sin IVA)
        if self.purchase.document_type == 'FACTURA':
            # Factura incluye IVA (19% en Chile)
            net_cost = self.total_cost / Decimal('1.19')
        else:
            # Boleta ya es neto
            net_cost = self.total_cost
        
        # Calcular costo neto por unidad base
        if quantity_in_base_units > 0:
            self.calculated_net_cost_per_base_unit = net_cost / quantity_in_base_units
        
        # Guardar el ítem
        super().save(*args, **kwargs)
        
        # Si es un nuevo ítem, actualizar el stock y costo del producto
        if is_new:
            self.product.update_stock_and_cost(
                quantity_change=quantity_in_base_units,
                new_item_cost=net_cost,
                new_quantity_in_base=quantity_in_base_units
            )
            
            # Publicar evento de actualización de stock (se implementará en tasks.py)
            from inventory.tasks import publish_product_stock_updated
            publish_product_stock_updated.delay(
                product_id=self.product.id,
                new_stock=float(self.product.current_stock),
                new_cost=float(self.product.average_cost)
            )


# ====================
# Signals para Señalización Digital
# ====================

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(post_save, sender=Product)
def product_saved_handler(sender, instance, created, **kwargs):
    """
    Signal que detecta cuando un producto es creado o modificado.
    Si el producto está activo en la web, envía el menú actualizado
    a todas las pantallas de TV conectadas vía WebSocket.
    
    Args:
        sender: Clase del modelo (Product)
        instance: Instancia del producto guardado
        created: True si es un nuevo producto
        **kwargs: Argumentos adicionales del signal
    """
    # Solo disparar actualización si el producto está activo en la web
    # o si acabamos de cambiar su estado
    if instance.is_active_website:
        # Importar aquí para evitar imports circulares
        from website_config.utils import get_public_menu_data
        
        # Obtener el channel layer
        channel_layer = get_channel_layer()
        
        if channel_layer:
            # Obtener el menú completo actualizado
            new_menu_data = get_public_menu_data()
            
            # Enviar el menú actualizado a todas las TVs conectadas
            async_to_sync(channel_layer.group_send)(
                'digital_signage',  # Nombre del grupo (debe coincidir con el Consumer)
                {
                    'type': 'signage_update',  # Llama al método signage_update del Consumer
                    'data': new_menu_data
                }
            )


@receiver(post_delete, sender=Product)
def product_deleted_handler(sender, instance, **kwargs):
    """
    Signal que detecta cuando un producto es eliminado.
    Envía el menú actualizado a todas las pantallas de TV.
    
    Args:
        sender: Clase del modelo (Product)
        instance: Instancia del producto eliminado
        **kwargs: Argumentos adicionales del signal
    """
    # Si el producto estaba en la web, actualizar pantallas
    if instance.is_active_website:
        from website_config.utils import get_public_menu_data
        
        channel_layer = get_channel_layer()
        
        if channel_layer:
            new_menu_data = get_public_menu_data()
            
            async_to_sync(channel_layer.group_send)(
                'digital_signage',
                {
                    'type': 'signage_update',
                    'data': new_menu_data
                }
            )


@receiver(post_save, sender=Category)
def category_saved_handler(sender, instance, **kwargs):
    """
    Signal que detecta cuando una categoría es modificada.
    Actualiza las pantallas si hay productos activos en esa categoría.
    """
    # Solo actualizar si hay productos activos en esta categoría
    if instance.products.filter(is_active_website=True).exists():
        from website_config.utils import get_public_menu_data
        
        channel_layer = get_channel_layer()
        
        if channel_layer:
            new_menu_data = get_public_menu_data()
            
            async_to_sync(channel_layer.group_send)(
                'digital_signage',
                {
                    'type': 'signage_update',
                    'data': new_menu_data
                }
            )
