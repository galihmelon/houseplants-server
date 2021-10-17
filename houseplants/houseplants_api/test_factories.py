from datetime import date, timedelta
import factory

from .models import Plant, WaterPlan


class PlantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plant

    name = factory.Faker('name')
    description = factory.Faker('text')
    image_url = factory.Faker('image_url')


class WaterPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WaterPlan

    plant = factory.SubFactory(PlantFactory)
    next_suggested_date = date.today() + timedelta(days=7)
