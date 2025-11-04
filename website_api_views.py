"""
Views para las APIs públicas del sitio web.
Endpoints accesibles sin autenticación para el frontend website.
"""

from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone

from inventory.models import Product, Category
from website_config.models import WebsiteSettings, GalleryImage
from blog.models import BlogPost
from legal.models import LegalPage
from reservations.models import Reservation
from loyalty_club.models import LoyaltyProgram, ClubMember

from website_api_serializers import (
    WebsiteSettingsSerializer,
    GalleryImageSerializer,
    CategorySimpleSerializer,
    WebMenuProductSerializer,
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    LegalPageSerializer,
    ReservationCreateSerializer,
    ReservationResponseSerializer,
    LoyaltyProgramSerializer,
    ClubMemberCreateSerializer,
    ClubMemberResponseSerializer,
)


# ==========================================
# Website Config Views
# ==========================================

class WebsiteConfigView(generics.RetrieveAPIView):
    """
    GET /api/website/config/
    Obtener la configuración pública del sitio web.
    """
    permission_classes = [AllowAny]
    serializer_class = WebsiteSettingsSerializer
    
    def get_object(self):
        return WebsiteSettings.load()


class GalleryImageListView(generics.ListAPIView):
    """
    GET /api/website/gallery/
    Obtener imágenes de la galería.
    """
    permission_classes = [AllowAny]
    serializer_class = GalleryImageSerializer
    
    def get_queryset(self):
        queryset = GalleryImage.objects.filter(is_active=True)
        
        # Filtrar por categoría si se proporciona
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__iexact=category)
        
        # Filtrar solo destacadas si se solicita
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset


# ==========================================
# Menu Views
# ==========================================

class WebMenuView(generics.GenericAPIView):
    """
    GET /api/website/menu/
    Obtener el menú público con productos activos para la web.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Obtener productos activos en la web
        products = Product.objects.filter(
            is_active=True,
            is_active_website=True
        ).select_related('category').order_by('display_order', 'category__name', 'name')
        
        # Filtrar por categoría si se proporciona
        category_id = request.query_params.get('category', None)
        if category_id:
            products = products.filter(category_id=category_id)
        
        # Obtener categorías que tienen productos activos
        categories = Category.objects.filter(
            products__is_active=True,
            products__is_active_website=True
        ).distinct().order_by('name')
        
        # Serializar
        product_serializer = WebMenuProductSerializer(
            products,
            many=True,
            context={'request': request}
        )
        category_serializer = CategorySimpleSerializer(categories, many=True)
        
        return Response({
            'categories': category_serializer.data,
            'products': product_serializer.data,
            'menu_title': WebsiteSettings.load().menu_title,
            'menu_description': WebsiteSettings.load().menu_description,
            'menu_footer_text': WebsiteSettings.load().menu_footer_text,
        })


# ==========================================
# Blog Views
# ==========================================

class BlogPostListView(generics.ListAPIView):
    """
    GET /api/website/blog/
    Listar posts publicados del blog.
    """
    permission_classes = [AllowAny]
    serializer_class = BlogPostListSerializer
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(
            status='published',
            published_date__lte=timezone.now()
        ).order_by('-published_date')
        
        # Filtrar por categoría si se proporciona
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__iexact=category)
        
        # Filtrar por tag si se proporciona
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__contains=[tag])
        
        # Buscar por texto
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        # Solo destacados
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset


class BlogPostDetailView(generics.RetrieveAPIView):
    """
    GET /api/website/blog/{slug}/
    Obtener detalle de un post del blog.
    """
    permission_classes = [AllowAny]
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(
            status='published',
            published_date__lte=timezone.now()
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Incrementar contador de vistas
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# ==========================================
# Legal Pages Views
# ==========================================

class LegalPageListView(generics.ListAPIView):
    """
    GET /api/website/legal/
    Listar páginas legales activas.
    """
    permission_classes = [AllowAny]
    serializer_class = LegalPageSerializer
    
    def get_queryset(self):
        return LegalPage.objects.filter(is_active=True).order_by('order', 'title')


class LegalPageDetailView(generics.RetrieveAPIView):
    """
    GET /api/website/legal/{slug}/
    Obtener una página legal específica.
    """
    permission_classes = [AllowAny]
    serializer_class = LegalPageSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return LegalPage.objects.filter(is_active=True)


# ==========================================
# Reservations Views
# ==========================================

class ReservationCreateView(generics.CreateAPIView):
    """
    POST /api/website/reservations/
    Crear una nueva reserva desde la web.
    """
    permission_classes = [AllowAny]
    serializer_class = ReservationCreateSerializer
    
    def create(self, request, *args, **kwargs):
        # Verificar que las reservas estén habilitadas
        settings = WebsiteSettings.load()
        if not settings.reservations_enabled:
            return Response(
                {'error': 'Las reservas no están disponibles en este momento.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save()
        
        # TODO: Enviar email de confirmación al cliente
        # TODO: Enviar notificación al restaurante
        
        response_serializer = ReservationResponseSerializer(reservation)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


# ==========================================
# Loyalty Club Views
# ==========================================

class LoyaltyProgramView(generics.RetrieveAPIView):
    """
    GET /api/website/loyalty-program/
    Obtener información del programa de fidelización.
    """
    permission_classes = [AllowAny]
    serializer_class = LoyaltyProgramSerializer
    
    def get_object(self):
        program = LoyaltyProgram.load()
        if not program.is_active:
            return Response(
                {'error': 'El programa de fidelización no está activo.'},
                status=status.HTTP_404_NOT_FOUND
            )
        return program


class ClubMemberCreateView(generics.CreateAPIView):
    """
    POST /api/website/loyalty-club/join/
    Inscribirse al club de fidelización.
    """
    permission_classes = [AllowAny]
    serializer_class = ClubMemberCreateSerializer
    
    def create(self, request, *args, **kwargs):
        # Verificar que el programa esté activo
        program = LoyaltyProgram.load()
        if not program.is_active:
            return Response(
                {'error': 'El programa de fidelización no está disponible en este momento.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        
        # TODO: Enviar email de bienvenida al nuevo miembro
        
        response_serializer = ClubMemberResponseSerializer(member)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
