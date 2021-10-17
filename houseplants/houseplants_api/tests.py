import pytest
from graphene.test import Client

from schema import schema


pytestmark = pytest.mark.django_db


def test_plants_to_care_query():
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
