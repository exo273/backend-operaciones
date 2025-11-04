"""
Serializers para las APIs públicas del sitio web.
Estos endpoints son consumidos por el frontend website.
"""

from rest_framework import serializers
from inventory.models import Product, Category
from website_config.models import WebsiteSettings, GalleryImage
from blog.models import BlogPost
from legal.models import LegalPage
from reservations.models import Reservation
from loyalty_club.models import LoyaltyProgram, ClubMember


# ==========================================
# Website Config Serializers
# ==========================================

class WebsiteSettingsSerializer(serializers.ModelSerializer):
    """Configuración pública del sitio web."""
    
    logo_url = serializers.SerializerMethodField()
    visible_pages = serializers.SerializerMethodField()
    
    class Meta:
        model = WebsiteSettings
        fields = [
            'site_name',
            'site_url',
            'tagline',
            'header_text',
            'logo_url',
            'footer_text',
            'footer_copyright',
            'primary_color',
            'secondary_color',
            'accent_color',
            'phone',
            'whatsapp',
            'email',
            'address',
            'opening_hours',
            'social_links',
            'google_maps_embed',
            'latitude',
            'longitude',
            'visible_pages',
            'meta_description',
            'meta_keywords',
            'google_analytics_id',
            'announcement_text',
            'announcement_active',
            'menu_title',
            'menu_description',
            'menu_footer_text',
            'reservations_enabled',
            'max_guests_per_reservation',
        ]
    
    def get_logo_url(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
    
    def get_visible_pages(self, obj):
        return obj.get_visible_pages()


class GalleryImageSerializer(serializers.ModelSerializer):
    """Imágenes de la galería."""
    
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryImage
        fields = [
            'id',
            'title',
            'image_url',
            'description',
            'category',
            'is_featured',
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


# ==========================================
# Menu Serializers
# ==========================================

class CategorySimpleSerializer(serializers.ModelSerializer):
    """Categoría simplificada para el menú web."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class WebMenuProductSerializer(serializers.ModelSerializer):
    """Productos para el menú web."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    image_url = serializers.SerializerMethodField()
    description_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description_display',
            'category_id',
            'category_name',
            'image_url',
            'web_price',
            'display_order',
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_description_display(self, obj):
        return obj.get_web_description()


# ==========================================
# Blog Serializers
# ==========================================

class BlogPostListSerializer(serializers.ModelSerializer):
    """Lista de posts del blog."""
    
    author_name = serializers.SerializerMethodField()
    featured_image_url = serializers.SerializerMethodField()
    excerpt_display = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'excerpt_display',
            'featured_image_url',
            'author_name',
            'category',
            'tags',
            'published_date',
            'views_count',
        ]
    
    def get_author_name(self, obj):
        return obj.get_author_display()
    
    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None
    
    def get_excerpt_display(self, obj):
        """Retorna el extracto o los primeros 200 caracteres del contenido."""
        if obj.excerpt:
            return obj.excerpt
        # Extraer primeros 200 caracteres del contenido
        if obj.content:
            return obj.content[:200] + '...' if len(obj.content) > 200 else obj.content
        return ''


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Detalle completo de un post del blog."""
    
    author_name = serializers.SerializerMethodField()
    featured_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'content',
            'featured_image_url',
            'author_name',
            'category',
            'tags',
            'published_date',
            'views_count',
            'meta_description',
        ]
    
    def get_author_name(self, obj):
        return obj.get_author_display()
    
    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None


# ==========================================
# Legal Pages Serializers
# ==========================================

class LegalPageSerializer(serializers.ModelSerializer):
    """Páginas legales."""
    
    class Meta:
        model = LegalPage
        fields = [
            'id',
            'title',
            'slug',
            'page_type',
            'content',
            'meta_description',
            'updated_at',
        ]


# ==========================================
# Reservations Serializers
# ==========================================

class ReservationCreateSerializer(serializers.ModelSerializer):
    """Crear una nueva reserva desde la web."""
    
    class Meta:
        model = Reservation
        fields = [
            'name',
            'phone',
            'email',
            'date',
            'time',
            'guests',
            'special_requests',
        ]
    
    def validate_guests(self, value):
        """Validar número de comensales."""
        settings = WebsiteSettings.load()
        if value > settings.max_guests_per_reservation:
            raise serializers.ValidationError(
                f'El número máximo de comensales es {settings.max_guests_per_reservation}.'
            )
        return value
    
    def create(self, validated_data):
        # Capturar IP si está disponible
        request = self.context.get('request')
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            validated_data['ip_address'] = ip
        
        return super().create(validated_data)


class ReservationResponseSerializer(serializers.ModelSerializer):
    """Respuesta después de crear una reserva."""
    
    class Meta:
        model = Reservation
        fields = [
            'id',
            'confirmation_code',
            'name',
            'date',
            'time',
            'guests',
            'status',
        ]


# ==========================================
# Loyalty Club Serializers
# ==========================================

class LoyaltyProgramSerializer(serializers.ModelSerializer):
    """Información del programa de fidelización."""
    
    class Meta:
        model = LoyaltyProgram
        fields = [
            'name',
            'description',
            'is_active',
            'benefits',
            'terms_and_conditions',
            'points_enabled',
        ]


class ClubMemberCreateSerializer(serializers.ModelSerializer):
    """Inscripción al club de fidelización."""
    
    class Meta:
        model = ClubMember
        fields = [
            'name',
            'email',
            'phone',
            'accepts_email_marketing',
            'accepts_sms_marketing',
        ]
    
    def validate_email(self, value):
        """Verificar que el email no esté ya registrado."""
        if ClubMember.objects.filter(email=value, status='active').exists():
            raise serializers.ValidationError('Este email ya está registrado en el club.')
        return value


class ClubMemberResponseSerializer(serializers.ModelSerializer):
    """Respuesta después de inscribirse al club."""
    
    class Meta:
        model = ClubMember
        fields = [
            'id',
            'member_code',
            'name',
            'email',
            'status',
            'join_date',
        ]
