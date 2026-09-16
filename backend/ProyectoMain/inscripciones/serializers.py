from rest_framework import serializers
from campanias.serializers import CampaniaSerializer
from usuarios.models import Usuario
from .models import Inscripcion


class UsuarioInscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'dni', 'email']


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


class InscripcionPropiaSerializer(serializers.ModelSerializer):
    campania = CampaniaSerializer(read_only=True)

    class Meta:
        model = Inscripcion
        fields = ['id', 'campania']
