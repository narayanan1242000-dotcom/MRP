# MRP System - Production Planning

A comprehensive Material Requirement Planning (MRP) system built with Django and Django REST Framework.

## Project Structure

```
MRP/
├── mrp_project/          # Django project settings
│   ├── settings.py       # Project configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
├── production/           # Production Planning Module
│   ├── models.py        # Database models
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── urls.py          # App URL routing
│   └── admin.py         # Django admin configuration
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── README.md            # This file
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/narayanan1242000-dotcom/MRP.git
cd MRP
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`
Admin panel: `http://localhost:8000/admin/`

## API Endpoints

### Vehicle Models
- `GET/POST /api/production/vehicle-models/` - List/Create vehicle models
- `GET/PUT/DELETE /api/production/vehicle-models/{id}/` - Retrieve/Update/Delete

### Production Plans
- `GET/POST /api/production/production-plans/` - List/Create production plans
- `GET/PUT/DELETE /api/production/production-plans/{id}/` - Retrieve/Update/Delete
- `GET /api/production/production-plans/daily_plans/` - Get daily plans
- `GET /api/production/production-plans/weekly_plans/` - Get weekly plans
- `GET /api/production/production-plans/model_wise_plans/` - Get model-wise plans
- `GET /api/production/production-plans/today_plan/` - Get today's plans
- `GET /api/production/production-plans/this_week_plan/` - Get this week's plans
- `GET /api/production/production-plans/summary/` - Get production summary
- `POST /api/production/production-plans/{id}/update_status/` - Update plan status
- `POST /api/production/production-plans/{id}/update_completed_quantity/` - Update completed qty

### Daily Production Plans
- `GET/POST /api/production/daily-plans/` - List/Create daily plans
- `GET/PUT/DELETE /api/production/daily-plans/{id}/` - Retrieve/Update/Delete

### Weekly Production Plans
- `GET/POST /api/production/weekly-plans/` - List/Create weekly plans
- `GET/PUT/DELETE /api/production/weekly-plans/{id}/` - Retrieve/Update/Delete

### Model-wise Production Plans
- `GET/POST /api/production/model-wise-plans/` - List/Create model-wise plans
- `GET/PUT/DELETE /api/production/model-wise-plans/{id}/` - Retrieve/Update/Delete
- `POST /api/production/model-wise-plans/{id}/calculate_percentage/` - Calculate completion %

## Features

### Step 1: Production Planning Screen ✅
- **Daily Plans**: Track production by shift (Shift A, B, C)
- **Weekly Plans**: Aggregate weekly production targets and tracking
- **Model-wise Plans**: Plan and track by vehicle model with completion percentage
- **Production Targets**: Set and monitor production targets
- **Status Tracking**: Plan states (PLANNED, IN_PROGRESS, COMPLETED, ON_HOLD, CANCELLED)

### Database Models

1. **VehicleModel** - Vehicle model master data
   - model_code (unique)
   - model_name
   - description
   - is_active

2. **ProductionPlan** - Main production planning
   - plan_id (unique)
   - plan_type (DAILY, WEEKLY, MODEL_WISE)
   - plan_date
   - vehicle_model (FK)
   - planned_quantity
   - completed_quantity
   - status
   - production_target
   - remarks

3. **DailyProductionPlan** - Daily shift-wise planning
   - production_plan (FK)
   - plan_date
   - shift (SHIFT_A, SHIFT_B, SHIFT_C)
   - planned_units
   - completed_units
   - defective_units

4. **WeeklyProductionPlan** - Weekly aggregation
   - production_plan (FK)
   - week_start_date
   - week_end_date
   - planned_units
   - completed_units
   - on_track

5. **ModelWiseProductionPlan** - Model-specific planning
   - production_plan (FK)
   - vehicle_model (FK)
   - planned_units
   - completed_units
   - percentage_complete

## Future Modules

- [ ] Step 2: BOM Module - Bill of Materials
- [ ] Step 3: MRP Calculation - Material requirement calculations
- [ ] Step 4: Material Shortage Report
- [ ] Step 5: Work Order Module
- [ ] Step 6: Dispatch Module
- [ ] Master Tables: Item, Supplier, Customer, Employee

## Technologies Used

- **Backend**: Django 4.2
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Django Auth
- **Filtering**: django-filter
- **CORS**: django-cors-headers

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit pull requests.
