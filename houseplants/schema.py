from datetime import date, timedelta
import graphene
from graphene_django import DjangoObjectType

from houseplants_api.models import Plant, WaterPlan
from houseplants_api.resolvers import (
    resolve_all_plants,
    resolve_plants_to_care,
)


class PlantType(DjangoObjectType):
    class Meta:
        model = Plant
        fields = ("id", "name", "image_url", "description")


class WaterPlanType(DjangoObjectType):
    class Meta:
        model = WaterPlan
        fields = ("plant", "water_date", "next_suggested_date")


class Query(graphene.ObjectType):
    all_plants = graphene.List(PlantType)
    plants_to_care = graphene.List(PlantType)

    def resolve_all_plants(root, info):
        return resolve_all_plants()

    def resolve_plants_to_care(root, info):
        return resolve_plants_to_care()


class WaterPlantMutation(graphene.Mutation):
    class Arguments:
        plant_id = graphene.ID()

    water_plan = graphene.Field(WaterPlanType)

    @classmethod
    def mutate(cls, root, info, plant_id):
        plant = Plant.objects.get(id=plant_id)
        plan = WaterPlan.objects.create(plant=plant, next_suggested_date=date.today() + timedelta(days=7))
        return WaterPlantMutation(water_plan=plan)


class Mutation(graphene.ObjectType):
    water_plant = WaterPlantMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
