from django.db import models
from django.conf import settings


class Site(models.Model):

    name = models.CharField(max_length=500)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    # TODO:
        # discussion
        # location
        # province
        # album
        # visitors
        # category
        # privilages
        # edit history?
        # status
        # value
        # hardness?
