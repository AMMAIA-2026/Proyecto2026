from rest_framework import serializers
from .models import Campania, CentroSalud, Estado_Campania
from datetime import date


class CentroSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroSalud
        fields = '__all__'


class CampaniaSerializer(serializers.ModelSerializer):

    estado_campania_texto = serializers.CharField(
        source='estado_campania.estado',
        read_only=True
        ) #campo adicional para mostrar el estado de la campaña como texto en lugar de solo el id

    estado_calculado = serializers.SerializerMethodField() #campo calculado para determinar el estado de la campaña en base a las fechas

    estado_campania = serializers.PrimaryKeyRelatedField(
        queryset=Estado_Campania.objects.all()
    )

    centro_salud = serializers.SerializerMethodField()
    centro_salud_id = serializers.PrimaryKeyRelatedField(
        source='centro_salud',
        queryset=CentroSalud.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    total_inscriptos = serializers.SerializerMethodField()


    class Meta:
        model = Campania
        fields = [
            'id',
            'titulo',
            'descripcion',
            'ubicacion',
            'fecha_inicio',
            'fecha_fin',
            'estado_campania',
            'estado_campania_texto',
            'estado_calculado',
            'centro_salud',
            'centro_salud_id',
            'cupo_maximo',
            'total_inscriptos',
        ]

    def get_estado_calculado(self, obj):
        hoy = date.today()
        if hoy < obj.fecha_inicio:
            return "Próximamente"
        elif hoy > obj.fecha_fin:
            return "Finalizada"
        return "En curso"

    def get_centro_salud(self, obj):
        if obj.centro_salud is None:
            return None
        return CentroSaludSerializer(obj.centro_salud).data

    def get_total_inscriptos(self, obj):
        return obj.inscripcion_set.count()
    


class EstadoCampaniaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estado_Campania
        fields = '__all__'
