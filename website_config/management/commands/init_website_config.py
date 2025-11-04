"""
Comando para inicializar la configuración del sitio web.
Uso: python manage.py init_website_config
"""

from django.core.management.base import BaseCommand
from website_config.models import WebsiteSettings
from loyalty_club.models import LoyaltyProgram


class Command(BaseCommand):
    help = 'Inicializa la configuración del sitio web con valores por defecto'
    
    def handle(self, *args, **options):
        # Crear o actualizar WebsiteSettings
        settings, created = WebsiteSettings.objects.get_or_create(id=1)
        
        if created:
            settings.site_name = "K'Vernicola"
            settings.site_url = "https://www.kvernicola.cl"
            settings.tagline = "Sabores Auténticos, Momentos Inolvidables"
            settings.phone = "+34 XXX XXX XXX"
            settings.email = "info@kvernicola.com"
            settings.address = "Calle Principal, 123, Ciudad"
            settings.opening_hours = {
                "monday": "Cerrado",
                "tuesday": "12:00 - 16:00, 20:00 - 23:00",
                "wednesday": "12:00 - 16:00, 20:00 - 23:00",
                "thursday": "12:00 - 16:00, 20:00 - 23:00",
                "friday": "12:00 - 16:00, 20:00 - 00:00",
                "saturday": "12:00 - 16:00, 20:00 - 00:00",
                "sunday": "12:00 - 16:00"
            }
            settings.social_links = {
                "facebook": "https://facebook.com/kvernicola",
                "instagram": "https://instagram.com/kvernicola",
                "twitter": "https://twitter.com/kvernicola"
            }
            settings.visible_pages = {
                "home": True,
                "menu": True,
                "gallery": True,
                "blog": True,
                "reservations": True,
                "loyalty_club": True,
                "contact": True
            }
            settings.meta_description = "Restaurante K'Vernicola - Cocina auténtica y momentos memorables en el corazón de la ciudad."
            settings.menu_title = "Nuestro Menú"
            settings.menu_description = "Descubre nuestra selección de platos elaborados con ingredientes frescos y de calidad."
            settings.reservations_enabled = True
            settings.reservations_email = "reservas@kvernicola.com"
            settings.max_guests_per_reservation = 10
            settings.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Configuración del sitio web creada exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠ La configuración del sitio web ya existe')
            )
        
        # Crear o actualizar LoyaltyProgram
        program, created = LoyaltyProgram.objects.get_or_create(id=1)
        
        if created:
            program.name = "Club K'Vernicola"
            program.description = "Únete a nuestro club de fidelización y disfruta de beneficios exclusivos."
            program.is_active = True
            program.benefits = [
                {
                    "title": "Descuentos Exclusivos",
                    "description": "10% de descuento en todos tus pedidos",
                    "icon": "tag"
                },
                {
                    "title": "Cumpleaños Especial",
                    "description": "Regalo especial el día de tu cumpleaños",
                    "icon": "gift"
                },
                {
                    "title": "Eventos VIP",
                    "description": "Invitaciones a eventos exclusivos del restaurante",
                    "icon": "star"
                },
                {
                    "title": "Acumula Puntos",
                    "description": "Gana puntos con cada visita y canjéalos por recompensas",
                    "icon": "trophy"
                }
            ]
            program.points_enabled = True
            program.points_per_euro = 10
            program.terms_and_conditions = "Los puntos caducan a los 12 meses de inactividad. Los beneficios son intransferibles."
            program.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Programa de fidelización creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠ El programa de fidelización ya existe')
            )
        
        self.stdout.write(
            self.style.SUCCESS('\n=== Inicialización completada ===')
        )
        self.stdout.write(
            self.style.SUCCESS('Ahora puedes personalizar la configuración desde el panel de administración.')
        )
