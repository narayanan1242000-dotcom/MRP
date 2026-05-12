from rest_framework import serializers
from .models import (
    VehicleModel,
    ProductionPlan,
    DailyProductionPlan,
    WeeklyProductionPlan,
    ModelWiseProductionPlan,
)


class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = ['id', 'model_code', 'model_name', 'description', 'is_active']


class DailyProductionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyProductionPlan
        fields = [
            'id', 'production_plan', 'plan_date', 'shift',
            'planned_units', 'completed_units', 'defective_units',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class WeeklyProductionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyProductionPlan
        fields = [
            'id', 'production_plan', 'week_start_date', 'week_end_date',
            'planned_units', 'completed_units', 'on_track',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ModelWiseProductionPlanSerializer(serializers.ModelSerializer):
    vehicle_model_data = VehicleModelSerializer(source='vehicle_model', read_only=True)

    class Meta:
        model = ModelWiseProductionPlan
        fields = [
            'id', 'production_plan', 'vehicle_model', 'vehicle_model_data',
            'planned_units', 'completed_units', 'percentage_complete',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProductionPlanSerializer(serializers.ModelSerializer):
    vehicle_model_data = VehicleModelSerializer(source='vehicle_model', read_only=True)
    daily_plans = DailyProductionPlanSerializer(many=True, read_only=True)
    weekly_plans = WeeklyProductionPlanSerializer(many=True, read_only=True)
    model_wise_plans = ModelWiseProductionPlanSerializer(many=True, read_only=True)

    class Meta:
        model = ProductionPlan
        fields = [
            'id', 'plan_id', 'plan_type', 'plan_date', 'vehicle_model',
            'vehicle_model_data', 'planned_quantity', 'completed_quantity',
            'status', 'production_target', 'remarks', 'created_by',
            'daily_plans', 'weekly_plans', 'model_wise_plans',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
