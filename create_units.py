"""
Script para crear unidades de medida básicas.
Ejecutar con: python manage.py shell < create_units.py
"""
from inventory.models import UnitOfMeasure

units = [
    {'name': 'Kilogramos', 'abbreviation': 'kg'},
    {'name': 'Gramos', 'abbreviation': 'g'},
    {'name': 'Litros', 'abbreviation': 'L'},
    {'name': 'Mililitros', 'abbreviation': 'ml'},
    {'name': 'Unidades', 'abbreviation': 'u'},
    {'name': 'Docenas', 'abbreviation': 'doc'},
    {'name': 'Paquetes', 'abbreviation': 'paq'},
    {'name': 'Cajas', 'abbreviation': 'caj'},
]

for unit_data in units:
    unit, created = UnitOfMeasure.objects.get_or_create(
        abbreviation=unit_data['abbreviation'],
        defaults={'name': unit_data['name']}
    )
    if created:
        print(f"✅ Creada: {unit.name} ({unit.abbreviation})")
    else:
        print(f"ℹ️  Ya existe: {unit.name} ({unit.abbreviation})")

print(f"\n📊 Total de unidades: {UnitOfMeasure.objects.count()}")
