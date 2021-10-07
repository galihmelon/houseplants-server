from datetime import date

from django.db.models import Max
import graphene
from graphene_django import DjangoObjectType

from houseplants_api.models import Plant, WaterPlan


class PlantType(DjangoObjectType):
    class Meta:
        model = Plant
        fields = ("id", "name", "image_url", "description")


class Query(graphene.ObjectType):
    all_plants = graphene.List(PlantType)
    plants_to_care = graphene.List(PlantType)

    def resolve_all_plants(root, info):
        return Plant.objects.all()

    def resolve_plants_to_care(root, info):
        plants = WaterPlan.objects.filter(next_suggested_date__lte=date.today()).values('plant').annotate(last_suggested_date=Max('next_suggested_date'))
        return Plant.objects.filter(id__in=[plant['plant'] for plant in plants])


schema = graphene.Schema(query=Query)
