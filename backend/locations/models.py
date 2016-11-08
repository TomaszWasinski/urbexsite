from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)


class Location(models.Model):
    ABANDONED = 'abandoned'
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    location_status = (
        (ABANDONED, 'Abandoned'),
        (INACTIVE, 'Non-existent'),
        (ACTIVE, 'Active'),
    )

    name = models.CharField(max_length=500)
    categories = models.ManyToManyField(Category)
    description = models.TextField()
    # coordinates = models.GeoPointField()
    status = models.CharField(max_length=10, choices=location_status, default=ABANDONED)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
