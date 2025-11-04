"""
Tareas de Celery para la aplicación Inventory.
Gestiona eventos de actualización de stock y consumo de eventos del bus.
"""

import json
import logging
from celery import shared_task
from kombu import Connection, Exchange, Queue
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


# Configuración del Event Bus
EVENT_EXCHANGE = Exchange('operations_events', type='topic', durable=True)
POS_EXCHANGE = Exchange('pos_events', type='topic', durable=True)


@shared_task(bind=True, max_retries=3)
def publish_product_stock_updated(self, product_id, new_stock, new_cost):
    """
    Publica un evento cuando el stock de un producto se actualiza.
    
    Args:
        product_id: ID del producto
        new_stock: Nuevo nivel de stock
        new_cost: Nuevo costo promedio
    """
    try:
        event_data = {
            'event_type': 'PRODUCT_STOCK_UPDATED',
            'product_id': product_id,
            'new_stock': new_stock,
            'new_cost': new_cost,
            'timestamp': str(timezone.now()),
        }
        
        with Connection(settings.EVENT_BUS_URL) as conn:
            producer = conn.Producer()
            producer.publish(
                event_data,
                exchange=EVENT_EXCHANGE,
                routing_key='product.stock.updated',
                serializer='json',
                retry=True,
            )
        
        logger.info(f"Evento PRODUCT_STOCK_UPDATED publicado para producto {product_id}")
        return {'status': 'success', 'product_id': product_id}
        
    except Exception as exc:
        logger.error(f"Error publicando evento de stock: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def process_order_paid(self, order_data):
    """
    Procesa un evento de orden pagada desde el servicio POS.
    Reduce el stock de los productos vendidos.
    
    Args:
        order_data: Datos de la orden pagada
            {
                'order_id': int,
                'items_sold': [
                    {'product_id': int, 'quantity': float},
                    ...
                ]
            }
    """
    from inventory.models import Product
    from django.db import transaction
    
    try:
        order_id = order_data.get('order_id')
        items_sold = order_data.get('items_sold', [])
        
        logger.info(f"Procesando orden pagada #{order_id} con {len(items_sold)} ítems")
        
        with transaction.atomic():
            for item in items_sold:
                product_id = item.get('product_id')
                quantity = item.get('quantity')
                
                try:
                    product = Product.objects.select_for_update().get(id=product_id)
                    
                    # Reducir stock
                    previous_stock = product.current_stock
                    product.update_stock_and_cost(
                        quantity_change=-quantity,
                        new_item_cost=None,
                        new_quantity_in_base=None
                    )
                    
                    logger.info(
                        f"Stock actualizado para producto {product.name}: "
                        f"{previous_stock} -> {product.current_stock}"
                    )
                    
                    # Publicar evento de actualización de stock
                    publish_product_stock_updated.delay(
                        product_id=product.id,
                        new_stock=float(product.current_stock),
                        new_cost=float(product.average_cost)
                    )
                    
                except Product.DoesNotExist:
                    logger.error(f"Producto {product_id} no encontrado para orden {order_id}")
                    continue
        
        return {'status': 'success', 'order_id': order_id}
        
    except Exception as exc:
        logger.error(f"Error procesando orden pagada: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task
def listen_pos_events():
    """
    Task que escucha eventos del servicio POS.
    Debe ser ejecutado como un worker persistente.
    """
    from django.utils import timezone
    
    queue = Queue(
        'pos_orders_queue',
        exchange=POS_EXCHANGE,
        routing_key='order.paid',
        durable=True
    )
    
    def process_message(body, message):
        """Callback para procesar mensajes recibidos."""
        try:
            logger.info(f"Evento recibido del POS: {body}")
            
            # Procesar la orden pagada
            process_order_paid.delay(body)
            
            # Acknowledge el mensaje
            message.ack()
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            message.reject()
    
    with Connection(settings.EVENT_BUS_URL) as conn:
        with conn.Consumer(queue, callbacks=[process_message]) as consumer:
            logger.info("Listener de eventos POS iniciado")
            while True:
                try:
                    conn.drain_events(timeout=1)
                except Exception as e:
                    logger.error(f"Error en listener: {e}")
                    continue


@shared_task
def check_low_stock_alerts():
    """
    Tarea programada para verificar productos con stock bajo.
    Puede ejecutarse periódicamente con Celery Beat.
    """
    from inventory.models import Product
    
    low_stock_products = Product.objects.filter(
        is_active=True,
        low_stock_threshold__isnull=False
    )
    
    alerts = []
    for product in low_stock_products:
        if product.is_low_stock:
            alerts.append({
                'product_id': product.id,
                'product_name': product.name,
                'current_stock': float(product.current_stock),
                'threshold': float(product.low_stock_threshold),
                'unit': product.inventory_unit.abbreviation,
            })
    
    if alerts:
        logger.warning(f"¡{len(alerts)} productos con stock bajo!")
        
        # Aquí se podría enviar una notificación, email, etc.
        # Por ahora solo logueamos
        for alert in alerts:
            logger.warning(
                f"Stock bajo: {alert['product_name']} - "
                f"Stock actual: {alert['current_stock']} {alert['unit']} "
                f"(umbral: {alert['threshold']})"
            )
    
    return {'total_alerts': len(alerts), 'alerts': alerts}
