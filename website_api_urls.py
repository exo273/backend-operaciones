"""
URLs para las APIs públicas del sitio web.
Estas rutas no requieren autenticación.
"""

from django.urls import path
from .website_api_views import (
    WebsiteConfigView,
    GalleryImageListView,
    WebMenuView,
    BlogPostListView,
    BlogPostDetailView,
    LegalPageListView,
    LegalPageDetailView,
    ReservationCreateView,
    LoyaltyProgramView,
    ClubMemberCreateView,
)

app_name = 'website_api'

urlpatterns = [
    # Configuración del sitio
    path('config/', WebsiteConfigView.as_view(), name='website-config'),
    
    # Galería
    path('gallery/', GalleryImageListView.as_view(), name='gallery-list'),
    
    # Menú público
    path('menu/', WebMenuView.as_view(), name='web-menu'),
    
    # Blog
    path('blog/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/<slug:slug>/', BlogPostDetailView.as_view(), name='blog-detail'),
    
    # Páginas legales
    path('legal/', LegalPageListView.as_view(), name='legal-list'),
    path('legal/<slug:slug>/', LegalPageDetailView.as_view(), name='legal-detail'),
    
    # Reservas
    path('reservations/', ReservationCreateView.as_view(), name='reservation-create'),
    
    # Club de fidelización
    path('loyalty-program/', LoyaltyProgramView.as_view(), name='loyalty-program'),
    path('loyalty-club/join/', ClubMemberCreateView.as_view(), name='club-member-join'),
]
