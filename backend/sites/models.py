from django.db import models
from django.conf import settings
from enum import Enum


class SiteStatus(Enum):
    active = "Active"
    inactive = "Non-existent"
    abandoned = "Abandoned"


class Categories(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)


class Site(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.CharField(max_length=10, choices=SiteStatus, default=SiteStatus.abandoned)
    score = models.PositiveSmallIntegerField(null=True)
    category = models.ManyToManyField(Categories)
    # TODO:
        # discussion
        # province
        # album
        # visitors OR visits (reverse)
        # privilages ??
        # edit history?
        # hardness?
    # more TODO:
    # privilages system

    def compute_score(self):
        pass # TODO after mergeing visits app
