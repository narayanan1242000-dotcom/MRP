from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VehicleModelViewSet,
    ProductionPlanViewSet,
    DailyProductionPlanViewSet,
    WeeklyProductionPlanViewSet,
    ModelWiseProductionPlanViewSet,
)

router = DefaultRouter()
router.register(r'vehicle-models', VehicleModelViewSet, basename='vehicle-model')
router.register(r'production-plans', ProductionPlanViewSet, basename='production-plan')
router.register(r'daily-plans', DailyProductionPlanViewSet, basename='daily-plan')
router.register(r'weekly-plans', WeeklyProductionPlanViewSet, basename='weekly-plan')
router.register(r'model-wise-plans', ModelWiseProductionPlanViewSet, basename='model-wise-plan')

urlpatterns = [
    path('', include(router.urls)),
]
