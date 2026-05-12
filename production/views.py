from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Q
from datetime import datetime, timedelta

from .models import (
    VehicleModel,
    ProductionPlan,
    DailyProductionPlan,
    WeeklyProductionPlan,
    ModelWiseProductionPlan,
)
from .serializers import (
    VehicleModelSerializer,
    ProductionPlanSerializer,
    DailyProductionPlanSerializer,
    WeeklyProductionPlanSerializer,
    ModelWiseProductionPlanSerializer,
)


class VehicleModelViewSet(viewsets.ModelViewSet):
    """API for Vehicle Model Master"""
    queryset = VehicleModel.objects.filter(is_active=True)
    serializer_class = VehicleModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['model_code', 'model_name']


class ProductionPlanViewSet(viewsets.ModelViewSet):
    """API for Production Planning"""
    queryset = ProductionPlan.objects.all()
    serializer_class = ProductionPlanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['plan_type', 'status', 'vehicle_model', 'plan_date']
    search_fields = ['plan_id', 'vehicle_model__model_code']
    ordering_fields = ['plan_date', 'created_at']
    ordering = ['-plan_date']

    @action(detail=False, methods=['get'])
    def daily_plans(self, request):
        """Get all daily production plans"""
        queryset = ProductionPlan.objects.filter(plan_type='DAILY')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def weekly_plans(self, request):
        """Get all weekly production plans"""
        queryset = ProductionPlan.objects.filter(plan_type='WEEKLY')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def model_wise_plans(self, request):
        """Get all model-wise production plans"""
        queryset = ProductionPlan.objects.filter(plan_type='MODEL_WISE')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update production plan status"""
        plan = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(ProductionPlan.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plan.status = new_status
        plan.save()
        return Response(
            {'message': f'Status updated to {new_status}'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def update_completed_quantity(self, request, pk=None):
        """Update completed quantity"""
        plan = self.get_object()
        completed_qty = request.data.get('completed_quantity')
        
        if completed_qty is None:
            return Response(
                {'error': 'completed_quantity is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if completed_qty > plan.planned_quantity:
            return Response(
                {'error': 'Completed quantity cannot exceed planned quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plan.completed_quantity = completed_qty
        plan.save()
        return Response(
            self.get_serializer(plan).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def today_plan(self, request):
        """Get today's production plans"""
        today = datetime.now().date()
        queryset = ProductionPlan.objects.filter(plan_date=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def this_week_plan(self, request):
        """Get this week's production plans"""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        queryset = ProductionPlan.objects.filter(
            plan_date__range=[week_start, week_end]
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get production summary statistics"""
        total_planned = ProductionPlan.objects.aggregate(
            total=Sum('planned_quantity')
        )['total'] or 0
        total_completed = ProductionPlan.objects.aggregate(
            total=Sum('completed_quantity')
        )['total'] or 0
        
        summary = {
            'total_planned': total_planned,
            'total_completed': total_completed,
            'pending': total_planned - total_completed,
            'completion_percentage': (
                (total_completed / total_planned * 100) if total_planned > 0 else 0
            ),
            'by_status': dict(
                ProductionPlan.objects.values('status').annotate(
                    count=Sum('planned_quantity')
                ).values_list('status', 'count')
            ),
        }
        return Response(summary)


class DailyProductionPlanViewSet(viewsets.ModelViewSet):
    """API for Daily Production Plans"""
    queryset = DailyProductionPlan.objects.all()
    serializer_class = DailyProductionPlanSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['plan_date', 'shift', 'production_plan']
    ordering_fields = ['plan_date', 'shift']
    ordering = ['-plan_date', 'shift']


class WeeklyProductionPlanViewSet(viewsets.ModelViewSet):
    """API for Weekly Production Plans"""
    queryset = WeeklyProductionPlan.objects.all()
    serializer_class = WeeklyProductionPlanSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['week_start_date', 'production_plan']
    ordering_fields = ['week_start_date']
    ordering = ['-week_start_date']


class ModelWiseProductionPlanViewSet(viewsets.ModelViewSet):
    """API for Model-wise Production Plans"""
    queryset = ModelWiseProductionPlan.objects.all()
    serializer_class = ModelWiseProductionPlanSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['vehicle_model', 'production_plan']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def calculate_percentage(self, request, pk=None):
        """Calculate and update completion percentage"""
        plan = self.get_object()
        percentage = plan.calculate_percentage()
        plan.save()
        return Response(
            {
                'vehicle_model': plan.vehicle_model.model_code,
                'planned_units': plan.planned_units,
                'completed_units': plan.completed_units,
                'percentage_complete': percentage
            },
            status=status.HTTP_200_OK
        )
