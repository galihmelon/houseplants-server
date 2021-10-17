from datetime import date
from django.db.models import Max

from .models import Plant, WaterPlan


def resolve_all_plants():
    return Plant.objects.all()


def resolve_plants_to_care():
    plants = WaterPlan.objects.filter(next_suggested_date__lte=date.today()).values('plant').annotate(last_suggested_date=Max('next_suggested_date'))
    return Plant.objects.filter(id__in=[plant['plant'] for plant in plants])
