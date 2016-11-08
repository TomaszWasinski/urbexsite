import pytest
from unittest.mock import patch
from datetime import datetime

from users.factories import UserFactory
from ..models import Location
from ..factories import LocationFactory


@pytest.mark.django_db
class LocationTests:

    def test_object_creation(self):
        location = Location(name='test_location', created_by=UserFactory())
        location.save()
        assert Location.objects.first().name == location.name

    def test_modified_field_is_updated_on_document_save(self):
        location = LocationFactory()
        with patch('locations.models.timezone.now') as tznow_mock:
            tznow_mock.return_value = datetime(1999, 1, 1)
            location.name = 'after this save modified field should get updated with upper'
            location.save()
        assert location.modified_at == datetime(1999, 1, 1)
