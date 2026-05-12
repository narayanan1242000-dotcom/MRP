from django.contrib import admin
from .models import (
    VehicleModel,
    ProductionPlan,
    DailyProductionPlan,
    WeeklyProductionPlan,
    ModelWiseProductionPlan,
)


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ['model_code', 'model_name', 'is_active', 'created_at']
    search_fields = ['model_code', 'model_name']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ProductionPlan)
class ProductionPlanAdmin(admin.ModelAdmin):
    list_display = [
        'plan_id', 'plan_type', 'vehicle_model', 'plan_date',
        'planned_quantity', 'completed_quantity', 'status'
    ]
    search_fields = ['plan_id', 'vehicle_model__model_code']
    list_filter = ['plan_type', 'status', 'plan_date']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Plan Information', {
            'fields': ('plan_id', 'plan_type', 'plan_date', 'vehicle_model')
        }),
        ('Quantities', {
            'fields': ('planned_quantity', 'completed_quantity', 'production_target')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'remarks', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DailyProductionPlan)
class DailyProductionPlanAdmin(admin.ModelAdmin):
    list_display = [
        'production_plan', 'plan_date', 'shift',
        'planned_units', 'completed_units', 'defective_units'
    ]
    search_fields = ['production_plan__plan_id', 'plan_date']
    list_filter = ['plan_date', 'shift']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(WeeklyProductionPlan)
class WeeklyProductionPlanAdmin(admin.ModelAdmin):
    list_display = [
        'production_plan', 'week_start_date', 'week_end_date',
        'planned_units', 'completed_units', 'on_track'
    ]
    search_fields = ['production_plan__plan_id', 'week_start_date']
    list_filter = ['week_start_date', 'on_track']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ModelWiseProductionPlan)
class ModelWiseProductionPlanAdmin(admin.ModelAdmin):
    list_display = [
        'production_plan', 'vehicle_model', 'planned_units',
        'completed_units', 'percentage_complete'
    ]
    search_fields = ['production_plan__plan_id', 'vehicle_model__model_code']
    list_filter = ['vehicle_model', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'percentage_complete']
