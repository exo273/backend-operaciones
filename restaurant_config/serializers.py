"""
Serializers para configuración del restaurante
"""
from rest_framework import serializers
from .models import RestaurantConfig


class RestaurantConfigSerializer(serializers.ModelSerializer):
    """Serializer para la configuración del restaurante"""
    logo_url = serializers.SerializerMethodField()
    receipt_logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = RestaurantConfig
        fields = [
            'id', 'name', 'logo', 'logo_url', 'receipt_logo', 'receipt_logo_url',
            'currency_symbol', 'language', 'address', 'phone', 'email', 'website',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_logo_url(self, obj):
        """Retorna la URL completa del logo"""
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
    
    def get_receipt_logo_url(self, obj):
        """Retorna la URL completa del logo de comanda"""
        if obj.receipt_logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.receipt_logo.url)
            return obj.receipt_logo.url
        return None
