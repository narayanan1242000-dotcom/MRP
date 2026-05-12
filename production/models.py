from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta


class VehicleModel(models.Model):
    """Vehicle Model Master"""
    model_code = models.CharField(max_length=50, unique=True, verbose_name='Model Code')
    model_name = models.CharField(max_length=100, verbose_name='Model Name')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model_code} - {self.model_name}"

    class Meta:
        verbose_name = 'Vehicle Model'
        verbose_name_plural = 'Vehicle Models'
        ordering = ['-created_at']


class ProductionPlan(models.Model):
    """Production Planning Screen"""
    PLAN_TYPE_CHOICES = [
        ('DAILY', 'Daily Plan'),
        ('WEEKLY', 'Weekly Plan'),
        ('MODEL_WISE', 'Model-wise Plan'),
    ]
    
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
        ('CANCELLED', 'Cancelled'),
    ]

    plan_id = models.CharField(max_length=100, unique=True, verbose_name='Plan ID')
    plan_type = models.CharField(
        max_length=20,
        choices=PLAN_TYPE_CHOICES,
        verbose_name='Plan Type'
    )
    plan_date = models.DateField(verbose_name='Plan Date')
    vehicle_model = models.ForeignKey(
        VehicleModel,
        on_delete=models.PROTECT,
        verbose_name='Vehicle Model'
    )
    planned_quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Planned Quantity'
    )
    completed_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Completed Quantity'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNED',
        verbose_name='Status'
    )
    production_target = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Production Target'
    )
    remarks = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=100, verbose_name='Created By')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.plan_id} - {self.vehicle_model} ({self.plan_date})"

    class Meta:
        verbose_name = 'Production Plan'
        verbose_name_plural = 'Production Plans'
        ordering = ['-plan_date']
        indexes = [
            models.Index(fields=['plan_date', 'vehicle_model']),
            models.Index(fields=['status']),
        ]


class DailyProductionPlan(models.Model):
    """Daily Production Plan Details"""
    production_plan = models.ForeignKey(
        ProductionPlan,
        on_delete=models.CASCADE,
        related_name='daily_plans',
        limit_choices_to={'plan_type': 'DAILY'}
    )
    plan_date = models.DateField(verbose_name='Plan Date')
    shift = models.CharField(
        max_length=20,
        choices=[('SHIFT_A', 'Shift A'), ('SHIFT_B', 'Shift B'), ('SHIFT_C', 'Shift C')],
        verbose_name='Shift'
    )
    planned_units = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Planned Units'
    )
    completed_units = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Completed Units'
    )
    defective_units = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Defective Units'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.plan_date} - {self.shift} - {self.planned_units} units"

    class Meta:
        verbose_name = 'Daily Production Plan'
        verbose_name_plural = 'Daily Production Plans'
        ordering = ['-plan_date', 'shift']
        unique_together = ['production_plan', 'plan_date', 'shift']


class WeeklyProductionPlan(models.Model):
    """Weekly Production Plan"""
    production_plan = models.ForeignKey(
        ProductionPlan,
        on_delete=models.CASCADE,
        related_name='weekly_plans',
        limit_choices_to={'plan_type': 'WEEKLY'}
    )
    week_start_date = models.DateField(verbose_name='Week Start Date')
    week_end_date = models.DateField(verbose_name='Week End Date')
    planned_units = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Planned Units'
    )
    completed_units = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Completed Units'
    )
    on_track = models.BooleanField(default=True, verbose_name='On Track')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Week {self.week_start_date} to {self.week_end_date} - {self.planned_units} units"

    class Meta:
        verbose_name = 'Weekly Production Plan'
        verbose_name_plural = 'Weekly Production Plans'
        ordering = ['-week_start_date']
        unique_together = ['production_plan', 'week_start_date']


class ModelWiseProductionPlan(models.Model):
    """Model-wise Production Plan"""
    production_plan = models.ForeignKey(
        ProductionPlan,
        on_delete=models.CASCADE,
        related_name='model_wise_plans',
        limit_choices_to={'plan_type': 'MODEL_WISE'}
    )
    vehicle_model = models.ForeignKey(
        VehicleModel,
        on_delete=models.PROTECT,
        verbose_name='Vehicle Model'
    )
    planned_units = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Planned Units'
    )
    completed_units = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Completed Units'
    )
    percentage_complete = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Percentage Complete'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle_model} - {self.planned_units} units"

    def calculate_percentage(self):
        """Calculate completion percentage"""
        if self.planned_units > 0:
            self.percentage_complete = (self.completed_units / self.planned_units) * 100
        return self.percentage_complete

    class Meta:
        verbose_name = 'Model-wise Production Plan'
        verbose_name_plural = 'Model-wise Production Plans'
        ordering = ['-created_at']
        unique_together = ['production_plan', 'vehicle_model']
