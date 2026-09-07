from rest_framework import serializers
from .models import Campania, EstadoCampaniaChoices
from centros_salud.serializers import CentroSaludSerializer
from django.utils import timezone

class CampaniaSerializer(serializers.ModelSerializer):

    estado_calculado = serializers.SerializerMethodField()
    total_inscriptos = serializers.SerializerMethodField()
    centro_salud_detalle = CentroSaludSerializer(
        source='centro_salud',
        read_only=True,
    )

    class Meta:
        model = Campania
        fields = '__all__'
        extra_kwargs = {
            'estado_campania': {'required': False}
        }

    def validate(self, attrs):
        fecha_inicio = attrs.get(
            'fecha_inicio',
            self.instance.fecha_inicio if self.instance else None
        )
        fecha_fin = attrs.get(
            'fecha_fin',
            self.instance.fecha_fin if self.instance else None
        )
        cupo_maximo = attrs.get(
            'cupo_maximo',
            self.instance.cupo_maximo if self.instance else None
        )
        hoy = timezone.localdate()

        if fecha_inicio is None or fecha_fin is None:
            return attrs

        #TODO. REVISAR VALIDEZ PARA NEGOCIO
        if self.instance is None and fecha_inicio < hoy:
            raise serializers.ValidationError({
                'fecha_inicio': 'La fecha de inicio no puede ser anterior a hoy.'
            })

        if (
            self.instance is not None
            and fecha_inicio < hoy
            and fecha_inicio != self.instance.fecha_inicio
        ):
            raise serializers.ValidationError({
                'fecha_inicio': 'La fecha de inicio no puede modificarse a una fecha anterior a hoy.'
            })

        if fecha_fin < hoy:
            raise serializers.ValidationError({
                'fecha_fin': 'No se puede crear o editar una campaña finalizada.'
            })

        if fecha_fin < fecha_inicio:
            raise serializers.ValidationError({
                'fecha_fin': 'La fecha de fin no puede ser anterior a la fecha de inicio.'
            })

        total_inscriptos = self.instance.inscripcion_set.count() if self.instance else 0
        attrs['estado_campania'] = self.calcular_estado(
            fecha_inicio,
            fecha_fin,
            cupo_maximo,
            total_inscriptos,
        )
        return attrs

    def get_estado_calculado(self, obj):
        return self.calcular_estado(
            obj.fecha_inicio,
            obj.fecha_fin,
            obj.cupo_maximo,
            self.get_total_inscriptos(obj),
        )

    def get_total_inscriptos(self, obj):
        total_anotado = getattr(obj, 'total_inscriptos_anotado', None)
        if total_anotado is not None:
            return total_anotado
        return obj.inscripcion_set.count()

    @staticmethod
    def calcular_estado(
        fecha_inicio,
        fecha_fin,
        cupo_maximo=None,
        total_inscriptos=0,
    ):
        hoy = timezone.localdate()
        if cupo_maximo is not None and total_inscriptos >= cupo_maximo:
            return EstadoCampaniaChoices.FINALIZADA
        if fecha_inicio > hoy:
            return EstadoCampaniaChoices.PROXIMAMENTE
        if fecha_fin >= hoy:
            return EstadoCampaniaChoices.ACTIVA
        return EstadoCampaniaChoices.FINALIZADA
