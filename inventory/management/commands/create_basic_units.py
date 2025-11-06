"""
Django management command to create basic units of measure.
Usage: python manage.py create_basic_units
"""
from django.core.management.base import BaseCommand
from inventory.models import UnitOfMeasure


class Command(BaseCommand):
    help = 'Creates basic units of measure for the inventory system'

    def handle(self, *args, **options):
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

        self.stdout.write(self.style.WARNING('Creating basic units of measure...'))
        self.stdout.write('')

        created_count = 0
        existing_count = 0

        for unit_data in units:
            unit, created = UnitOfMeasure.objects.get_or_create(
                abbreviation=unit_data['abbreviation'],
                defaults={'name': unit_data['name']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Created: {unit.name} ({unit.abbreviation})")
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f"• Already exists: {unit.name} ({unit.abbreviation})")
                )
                existing_count += 1

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {created_count + existing_count} units:')
        )
        self.stdout.write(f'  - Created: {created_count}')
        self.stdout.write(f'  - Already existed: {existing_count}')
        self.stdout.write(f'  - Total in database: {UnitOfMeasure.objects.count()}')
