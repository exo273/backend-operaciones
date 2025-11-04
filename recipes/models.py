"""
Modelos de la aplicación Recipes.
Gestiona recetas y sus ingredientes con cálculo automático de costos.
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db import transaction


class Recipe(models.Model):
    """Receta de producción."""
    
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Nombre"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    instructions = models.TextField(
        blank=True,
        verbose_name="Instrucciones de Preparación"
    )
    yield_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Cantidad de Rendimiento",
        help_text="Cantidad que produce esta receta"
    )
    yield_unit = models.CharField(
        max_length=50,
        verbose_name="Unidad de Rendimiento",
        help_text="Ej: Litros, Unidades, Porciones"
    )
    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Costo Total",
        help_text="Calculado automáticamente"
    )
    cost_per_unit = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=Decimal('0.0000'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Costo por Unidad",
        help_text="Calculado automáticamente"
    )
    preparation_time = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Tiempo de Preparación (minutos)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.yield_quantity} {self.yield_unit})"

    def calculate_cost(self):
        """
        Calcula el costo total de la receta sumando el costo de todos sus ingredientes.
        """
        with transaction.atomic():
            total = Decimal('0.00')
            
            for ingredient in self.ingredients.all():
                ingredient_cost = ingredient.calculate_cost()
                total += ingredient_cost
            
            self.total_cost = total
            
            # Calcular costo por unidad
            if self.yield_quantity > 0:
                self.cost_per_unit = self.total_cost / self.yield_quantity
            else:
                self.cost_per_unit = Decimal('0.0000')
            
            self.save(update_fields=['total_cost', 'cost_per_unit', 'updated_at'])
            
            return total

    def save(self, *args, **kwargs):
        """Al guardar, recalcular costos si ya tiene ingredientes."""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Si no es nueva, recalcular costos
        if not is_new:
            self.calculate_cost()
            
            # Publicar evento de actualización de receta
            from recipes.tasks import publish_recipe_updated
            publish_recipe_updated.delay(
                recipe_id=self.id,
                recipe_name=self.name,
                total_cost=float(self.total_cost),
                cost_per_unit=float(self.cost_per_unit)
            )


class RecipeIngredient(models.Model):
    """Ingrediente en una receta."""
    
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name="Receta"
    )
    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.PROTECT,
        related_name='recipe_ingredients',
        verbose_name="Producto"
    )
    quantity_needed = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Cantidad Necesaria"
    )
    unit = models.CharField(
        max_length=50,
        verbose_name="Unidad",
        help_text="Unidad usada en la receta (debe ser compatible con la unidad base del producto)"
    )
    conversion_factor = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        default=Decimal('1.000000'),
        validators=[MinValueValidator(Decimal('0.000001'))],
        verbose_name="Factor de Conversión",
        help_text="Factor para convertir de la unidad de la receta a la unidad base del producto"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notas"
    )
    calculated_cost = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=Decimal('0.0000'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Costo Calculado",
        help_text="Calculado automáticamente"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ingrediente de Receta"
        verbose_name_plural = "Ingredientes de Receta"
        ordering = ['recipe', 'product']
        unique_together = [['recipe', 'product']]

    def __str__(self):
        return f"{self.product.name} - {self.quantity_needed} {self.unit}"

    def calculate_cost(self):
        """
        Calcula el costo de este ingrediente basándose en:
        - Cantidad necesaria
        - Factor de conversión a unidad base
        - Costo promedio del producto
        """
        # Convertir cantidad a unidades base
        quantity_in_base_units = self.quantity_needed * self.conversion_factor
        
        # Calcular costo
        cost = quantity_in_base_units * self.product.average_cost
        
        self.calculated_cost = cost
        return cost

    def save(self, *args, **kwargs):
        """Al guardar, calcular el costo y actualizar el costo total de la receta."""
        # Calcular el costo de este ingrediente
        self.calculate_cost()
        
        # Guardar el ingrediente
        super().save(*args, **kwargs)
        
        # Recalcular el costo total de la receta
        self.recipe.calculate_cost()

    def delete(self, *args, **kwargs):
        """Al eliminar, actualizar el costo total de la receta."""
        recipe = self.recipe
        super().delete(*args, **kwargs)
        recipe.calculate_cost()
