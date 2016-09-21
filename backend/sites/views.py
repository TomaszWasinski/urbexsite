from django.shortcuts import render

from rest_framework.viewsets import ReadOnlyModelViewSet


class SitesViewSet(ReadOnlyModelViewSet):  # Temporarely ReadOnly

    queryset = Sites.objects.all()
    
