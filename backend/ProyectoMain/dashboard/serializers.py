from rest_framework import serializers
from campanias.models import Campania
from campanias.serializers import CampaniaSerializer


class InscripcionPorMesSerializer(serializers.Serializer):
    anio = serializers.IntegerField()
    mes = serializers.IntegerField()
    cantidad = serializers.IntegerField()


class DonantesPorMesSerializer(serializers.Serializer):
    anio = serializers.IntegerField()
    mes = serializers.IntegerField()
    cantidad = serializers.IntegerField()


class CampaniasPorEstadoSerializer(serializers.Serializer):
    estado = serializers.CharField()
    cantidad = serializers.IntegerField()


class CampaniaRecienteSerializer(CampaniaSerializer):
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Campania
        fields = [
            'id',
            'titulo',
            'descripcion',
            'ubicacion',
            'centro_salud',
            'centro_salud_detalle',
            'fecha_inicio',
            'fecha_fin',
            'cupo_maximo',
            'total_inscriptos',
            'estado_campania',
            'estado_calculado',
            'estado',
        ]

    def get_estado(self, obj):
        return self.get_estado_calculado(obj)


class DashboardSerializer(serializers.Serializer):
    total_campanias = serializers.IntegerField()
    total_inscripciones = serializers.IntegerField()
    total_donantes = serializers.IntegerField()
    campanias_recientes = CampaniaRecienteSerializer(many=True)
    campanias_por_estado = CampaniasPorEstadoSerializer(many=True)
    inscripciones_por_mes = InscripcionPorMesSerializer(many=True)
    donantes_por_mes = DonantesPorMesSerializer(many=True)
