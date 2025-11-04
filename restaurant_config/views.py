"""
Views para configuración del restaurante
"""
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import RestaurantConfig
from .serializers import RestaurantConfigSerializer


class RestaurantConfigViewSet(viewsets.ViewSet):
    """
    ViewSet para configuración del restaurante (Singleton)
    Solo permite GET y PATCH, no POST ni DELETE
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RestaurantConfigSerializer
    
    def list(self, request):
        """
        GET /api/operations/config/
        Obtiene la configuración única del restaurante
        """
        config = RestaurantConfig.load()
        serializer = RestaurantConfigSerializer(config, context={'request': request})
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        """
        PATCH /api/operations/config/1/
        Actualiza la configuración del restaurante
        Solo admins pueden actualizar
        """
        if not request.user.is_staff:
            return Response({
                'detail': 'No tienes permiso para actualizar la configuración.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        config = RestaurantConfig.load()
        serializer = RestaurantConfigSerializer(
            config, 
            data=request.data, 
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        GET /api/operations/config/current/
        Alias para obtener la configuración actual
        """
        return self.list(request)
