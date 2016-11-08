import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.factories import UserFactory
from ..models import Location
from ..factories import LocationFactory, CategoryFactory


client = APIClient()


@pytest.fixture
def authenticated_client(request):
    user = UserFactory()
    client.force_authenticate(user=user)
    yield client
    client.logout()


@pytest.mark.django_db
class LocationViewListTests:

    @pytest.fixture
    def url(self, request):
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


@pytest.mark.django_db
class LocationViewCreateTests:

    @pytest.fixture
    def url(self, request):
        return '/api/locations/'

    def test_only_authenticated_users_can_post(self, url):
        response = client.post(url, {'name': 'location1', 'description': 'something', 'status': 'abandoned'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_location_creation(self, url, authenticated_client):
        response = authenticated_client.post(url, {'name': 'location1', 'description': 'something', 'status': 'abandoned'})
        assert response.status_code == status.HTTP_201_CREATED
