import pytest
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Location
from ..factories import LocationFactory, CategoryFactory


client = APIClient()


@pytest.mark.django_db
class SiteViewSetTests:

    @pytest.fixture
    def url(request):
        return '/api/locations/'

    def test_list_view_on_empty_collection(self, url):
        """ no data was created """
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_list_view_with_1_object_created(self, url):
        LocationFactory()
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
