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


class Query(graphene.ObjectType):
    all_plants = graphene.List(PlantType)
    plants_to_care = graphene.List(PlantType)

    def resolve_all_plants(root, info):
        return resolve_all_plants()

    def resolve_plants_to_care(root, info):
        return resolve_plants_to_care()


schema = graphene.Schema(query=Query)
