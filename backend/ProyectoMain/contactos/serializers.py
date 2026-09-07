from rest_framework import serializers

from .models import Contacto


class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = [
            'id',
            'email',
            'asunto',
            'mensaje',
            'tracked',
            'fecha_creacion',
        ]
        read_only_fields = ['id', 'tracked', 'fecha_creacion']


class ContactoTrackedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = ['tracked']
