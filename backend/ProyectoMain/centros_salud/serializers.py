from rest_framework import serializers

from .models import CentroSalud


class CentroSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroSalud
        fields = '__all__'
