"""
WebSocket Consumer para señalización digital.
Maneja las conexiones en tiempo real con las pantallas de TV.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .utils import get_public_menu_data


class SignageConsumer(AsyncWebsocketConsumer):
    """
    Consumer que maneja la conexión WebSocket para señalización digital.
    
    Las TVs se conectan a este consumer y reciben:
    - El menú completo al conectarse
    - Actualizaciones en tiempo real cuando cambian productos
    """
    
    async def connect(self):
        """
        Maneja la conexión inicial de una TV.
        - Une la conexión al grupo 'digital_signage'
        - Envía el menú actual inmediatamente
        """
        # Todos los clientes se unen al mismo grupo por ahora
        # En modo multi-tenant, esto sería dinámico por restaurante
        self.room_group_name = 'digital_signage'
        
        # Unirse al grupo de channel layer
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Aceptar la conexión WebSocket
        await self.accept()
        
        # Enviar el menú actual inmediatamente al conectarse
        current_menu_data = await self.get_menu()
        await self.send(text_data=json.dumps({
            'type': 'menu_update',
            'data': current_menu_data,
            'timestamp': self._get_timestamp(),
        }))
    
    async def disconnect(self, close_code):
        """
        Maneja la desconexión de una TV.
        - Remueve la conexión del grupo
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def signage_update(self, event):
        """
        Maneja mensajes del tipo 'signage_update' desde el channel layer.
        Este método es llamado cuando un signal de Django detecta cambios.
        
        Args:
            event (dict): Evento con la estructura:
                {
                    'type': 'signage_update',
                    'data': {...menu data...}
                }
        """
        # Reenviar el menú actualizado a la TV conectada
        await self.send(text_data=json.dumps({
            'type': 'menu_update',
            'data': event['data'],
            'timestamp': self._get_timestamp(),
        }))
    
    @database_sync_to_async
    def get_menu(self):
        """
        Obtiene el menú desde la base de datos de forma asíncrona.
        
        Returns:
            dict: Menú completo con categorías y productos
        """
        return get_public_menu_data()
    
    @staticmethod
    def _get_timestamp():
        """
        Genera un timestamp ISO 8601 para el mensaje.
        
        Returns:
            str: Timestamp en formato ISO
        """
        from datetime import datetime
        return datetime.now().isoformat()
