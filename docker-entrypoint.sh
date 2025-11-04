#!/bin/bash
set -e

# Esperar a que la base de datos esté lista
echo "Esperando a que la base de datos esté lista..."
python << END
import sys
import time
import os
import MySQLdb

max_attempts = 30
attempt = 0

while attempt < max_attempts:
    try:
        conn = MySQLdb.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', ''),
            port=int(os.environ.get('DB_PORT', 3306))
        )
        conn.close()
        print("¡Base de datos lista!")
        sys.exit(0)
    except Exception as e:
        attempt += 1
        print(f"Intento {attempt}/{max_attempts}: {e}")
        time.sleep(2)

print("No se pudo conectar a la base de datos")
sys.exit(1)
END

# Crear migraciones para todas las apps
echo "Creando migraciones..."
python manage.py makemigrations suppliers inventory recipes website_config blog legal reservations loyalty_club

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput --fake-initial

# Crear superusuario si no existe
echo "Verificando superusuario..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superusuario creado")
else:
    print("Superusuario ya existe")
END

# Determinar qué proceso ejecutar basado en el argumento
if [ "$1" = "worker" ]; then
    echo "Iniciando Celery Worker..."
    exec celery -A operations_service worker -l info
elif [ "$1" = "beat" ]; then
    echo "Iniciando Celery Beat..."
    exec celery -A operations_service beat -l info
else
    echo "Iniciando servidor Gunicorn..."
    exec gunicorn operations_service.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
fi
