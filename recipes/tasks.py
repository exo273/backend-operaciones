"""
Tareas de Celery para la aplicación Recipes.
Gestiona eventos de actualización de recetas.
"""

import logging
from celery import shared_task
from kombu import Connection, Exchange
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

# Configuración del Event Bus
EVENT_EXCHANGE = Exchange('operations_events', type='topic', durable=True)


@shared_task(bind=True, max_retries=3)
def publish_recipe_updated(self, recipe_id, recipe_name, total_cost, cost_per_unit):
    """
    Publica un evento cuando una receta se actualiza.
    
    Args:
        recipe_id: ID de la receta
        recipe_name: Nombre de la receta
        total_cost: Costo total de la receta
        cost_per_unit: Costo por unidad de la receta
    """
    try:
        event_data = {
            'event_type': 'RECIPE_UPDATED',
            'recipe_id': recipe_id,
            'recipe_name': recipe_name,
            'total_cost': total_cost,
            'cost_per_unit': cost_per_unit,
            'timestamp': str(timezone.now()),
        }
        
        with Connection(settings.EVENT_BUS_URL) as conn:
            producer = conn.Producer()
            producer.publish(
                event_data,
                exchange=EVENT_EXCHANGE,
                routing_key='recipe.updated',
                serializer='json',
                retry=True,
            )
        
        logger.info(f"Evento RECIPE_UPDATED publicado para receta {recipe_id}: {recipe_name}")
        return {'status': 'success', 'recipe_id': recipe_id}
        
    except Exception as exc:
        logger.error(f"Error publicando evento de receta: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task
def recalculate_all_recipe_costs():
    """
    Tarea programada para recalcular los costos de todas las recetas activas.
    Útil cuando hay cambios masivos en los costos de productos.
    """
    from recipes.models import Recipe
    
    recipes = Recipe.objects.filter(is_active=True)
    updated_count = 0
    
    for recipe in recipes:
        try:
            old_cost = recipe.total_cost
            new_cost = recipe.calculate_cost()
            
            if old_cost != new_cost:
                updated_count += 1
                logger.info(
                    f"Receta '{recipe.name}' actualizada: "
                    f"${old_cost} -> ${new_cost}"
                )
                
                # Publicar evento
                publish_recipe_updated.delay(
                    recipe_id=recipe.id,
                    recipe_name=recipe.name,
                    total_cost=float(new_cost),
                    cost_per_unit=float(recipe.cost_per_unit)
                )
                
        except Exception as e:
            logger.error(f"Error recalculando receta {recipe.id}: {e}")
            continue
    
    return {
        'total_recipes': recipes.count(),
        'updated_count': updated_count,
    }
