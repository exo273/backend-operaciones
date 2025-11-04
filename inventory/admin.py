from django.contrib import admin
from .models import Category, UnitOfMeasure, Product, PurchaseUnit, Purchase, PurchaseItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'created_at']
    search_fields = ['name', 'abbreviation']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'current_stock', 'inventory_unit', 'average_cost', 'is_low_stock', 'is_active']
    list_filter = ['category', 'is_active', 'inventory_unit']
    search_fields = ['name', 'description']
    readonly_fields = ['current_stock', 'average_cost', 'created_at', 'updated_at']


@admin.register(PurchaseUnit)
class PurchaseUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_unit', 'conversion_factor', 'created_at']
    search_fields = ['name']


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    readonly_fields = ['calculated_net_cost_per_base_unit']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'document_type', 'supplier', 'purchase_date', 'total_amount', 'created_at']
    list_filter = ['document_type', 'purchase_date', 'supplier']
    search_fields = ['document_number', 'supplier__name']
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    inlines = [PurchaseItemInline]
    date_hierarchy = 'purchase_date'


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'product', 'quantity_purchased', 'purchase_unit', 'total_cost', 'calculated_net_cost_per_base_unit']
    list_filter = ['purchase__purchase_date', 'product__category']
    search_fields = ['product__name', 'purchase__document_number']
    readonly_fields = ['calculated_net_cost_per_base_unit', 'created_at', 'updated_at']
