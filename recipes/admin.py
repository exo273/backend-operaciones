from django.contrib import admin
from .models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    readonly_fields = ['calculated_cost']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'yield_quantity', 'yield_unit', 'total_cost', 'cost_per_unit', 'is_active', 'updated_at']
    list_filter = ['is_active', 'yield_unit']
    search_fields = ['name', 'description']
    readonly_fields = ['total_cost', 'cost_per_unit', 'created_at', 'updated_at']
    inlines = [RecipeIngredientInline]
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Rendimiento', {
            'fields': ('yield_quantity', 'yield_unit')
        }),
        ('Costos', {
            'fields': ('total_cost', 'cost_per_unit'),
            'classes': ('collapse',)
        }),
        ('Preparación', {
            'fields': ('instructions', 'preparation_time')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'product', 'quantity_needed', 'unit', 'conversion_factor', 'calculated_cost']
    list_filter = ['recipe', 'product__category']
    search_fields = ['recipe__name', 'product__name']
    readonly_fields = ['calculated_cost', 'created_at', 'updated_at']
