from rest_framework import serializers

from .models import Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'name', 'description', 'status', 'created_by',
                  'created_at', 'modified_at')
        read_only_fields = ('created_by', 'created_at', 'modified_at')
