import pytest
from utils.fixtures import mongomock

from ..models import Site


@pytest.mark.usefixtures('mongomock')
class SiteTests:

    def test_object_creation(self):
        site = Site(name='test_site')
        site.save()
        assert Site.objects.first().name == site.name

    def test_object_creation2(self):
        site = Site(name='test_site2')
        site.save()
        assert Site.objects.first().name == site.name

    def test_object_creation3(self):
        site = Site(name='test_site3')
        site.save()
        assert Site.objects.first().name == site.name
