from datetime import date, timedelta
import pytest
from graphene.test import Client

from schema import schema
from .test_factories import PlantFactory, WaterPlanFactory


pytestmark = pytest.mark.django_db


def test_plants_to_care_query_with_empty_result():
    client = Client(schema)
    executed = client.execute(
        '''
        query {
            plantsToCare {
                id
                name
                imageUrl
                description
            }
        }
        '''
    )
    assert executed == {
        'data': {
            'plantsToCare': []
        }
    }


def test_plants_to_care_query_with_results():
    plan_a = WaterPlanFactory(next_suggested_date=date.today())
    plan_b = WaterPlanFactory(next_suggested_date=date.today() - timedelta(days=3))
    plan_c = WaterPlanFactory(next_suggested_date=date.today() + timedelta(days=3))

    client = Client(schema)
    executed = client.execute(
        '''
        query {
            plantsToCare {
                id
                name
                imageUrl
                description
            }
        }
        '''
    )
    plants_to_care = executed['data']['plantsToCare']
    assert len(plants_to_care) == 2

    plant_ids = [int(plant['id']) for plant in plants_to_care]
    assert plant_ids == [plan_a.plant.id, plan_b.plant.id]


def test_water_plant_mutation():
    plant = PlantFactory(id=1)

    client = Client(schema)
    executed = client.execute(
        '''
        mutation {
            waterPlant(plantId: 1) {
                waterPlan {
                plant {
                    id
                }
                nextSuggestedDate
                waterDate
                }
            }
        }
        '''
    )
    plan = executed['data']['waterPlant']['waterPlan']
    assert plan['plant']['id'] == '1'
    assert plan['waterDate'] == date.today().strftime('%Y-%m-%d')
