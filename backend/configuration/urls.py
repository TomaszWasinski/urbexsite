from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from locations.views import LocationViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/accounts/', include('rest_auth.urls')),
    url(r'^api/accounts/registration/', include('rest_auth.registration.urls')),
    url(r'^admin/', admin.site.urls),
]
