"""
Configuración de Celery para operations_service.
"""

import os
from celery import Celery

# Configurar el módulo de settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'operations_service.settings')

app = Celery('operations_service')

# Usar la configuración de Django para Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubrir tareas en todas las apps instaladas
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Tarea de debug para probar Celery."""
    print(f'Request: {self.request!r}')
