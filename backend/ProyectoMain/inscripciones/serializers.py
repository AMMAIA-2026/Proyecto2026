from rest_framework import serializers
from .models import Inscripcion

class InscripcionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Inscripcion

        fields = [
            'id',
            'campania',
            'fecha_inscripcion',
            'usuario'
        ]

        read_only_fields = [
            'id',
            'campania',
            'usuario',
            'fecha_inscripcion'
        ]
