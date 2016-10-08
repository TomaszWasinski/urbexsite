import mongoengine as me
from django.db import models
from django.conf import settings
from django.utils import timezone
from enum import Enum


class SiteStatus(Enum):
    active = "Active"
    inactive = "Non-existent"
    abandoned = "Abandoned"


class Categories(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)


class Site(me.Document):
    name = me.StringField(max_length=500, required=True)
    description = me.StringField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.CharField(max_length=10, choices=SiteStatus, default=SiteStatus.abandoned)
    score = models.PositiveSmallIntegerField(null=True)
    category = mo
    created_by =
    updated_by =
    created = me.DateTimeField(required=True)
    modified = me.DateTimeField(required=timezone.now)
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
        pass  # TODO after mergeing visits app
