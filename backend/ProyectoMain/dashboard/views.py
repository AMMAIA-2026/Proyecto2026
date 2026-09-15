from datetime import datetime, time, timedelta
from django.db.models import Case, Count, DateField, F, IntegerField, Q, Value, When
from django.db.models.functions import Cast, ExtractMonth, ExtractYear
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from campanias.models import Campania, EstadoCampaniaChoices
from campanias.serializers import CampaniaSerializer
from inscripciones.models import Inscripcion
from usuarios.models import RolChoices
from usuarios.permissions import EsAdministrador
from .serializers import DashboardSerializer


class DashboardView(APIView):
    permission_classes = [EsAdministrador]

    def get(self, request):
        hoy = timezone.localdate()
        inicio_mes_actual = hoy.replace(day=1)
        inicio_periodo = inicio_mes_actual

        for _ in range(11):
            inicio_periodo = (inicio_periodo - timedelta(days=1)).replace(day=1)

        if inicio_mes_actual.month == 12:
            fin_periodo = inicio_mes_actual.replace(
                year=inicio_mes_actual.year + 1, month=1
            )
        else:
            fin_periodo = inicio_mes_actual.replace(month=inicio_mes_actual.month + 1)

        zona_horaria = timezone.get_current_timezone()
        inicio_periodo_datetime = timezone.make_aware(
            datetime.combine(inicio_periodo, time.min), zona_horaria
        )
        fin_periodo_datetime = timezone.make_aware(
            datetime.combine(fin_periodo, time.min), zona_horaria
        )

        inscripciones_periodo = Inscripcion.objects.filter(
            fecha_inscripcion__gte=inicio_periodo_datetime,
            fecha_inscripcion__lt=fin_periodo_datetime,
        ).annotate(
            fecha=Cast('fecha_inscripcion', output_field=DateField()),
        ).annotate(
            anio=ExtractYear('fecha'),
            mes=ExtractMonth('fecha'),
        )

        total_campanias = Campania.objects.count()
        total_inscripciones = Inscripcion.objects.count()
        total_donantes = (
            Inscripcion.objects
            .filter(usuario__rol=RolChoices.USUARIO_ESTANDAR)
            .values('usuario_id')
            .distinct()
            .count()
        )
        conteo_estados = {}
        campanias_con_totales = (
            Campania.objects
            .annotate(total_inscriptos=Count('inscripcion'))
            .values(
                'fecha_inicio',
                'fecha_fin',
                'cupo_maximo',
                'total_inscriptos',
            )
        )
        for campania in campanias_con_totales:
            estado = CampaniaSerializer.calcular_estado(
                campania['fecha_inicio'],
                campania['fecha_fin'],
                campania['cupo_maximo'],
                campania['total_inscriptos'],
            )
            conteo_estados[estado] = conteo_estados.get(estado, 0) + 1

        campanias_por_estado = [
            {'estado': estado, 'cantidad': cantidad}
            for estado, cantidad in sorted(conteo_estados.items())
        ]
        campanias_recientes = (
            Campania.objects.select_related('centro_salud')
            .annotate(total_inscriptos_anotado=Count('inscripcion'))
            .filter(
                fecha_fin__gte=hoy,
            )
            .filter(
                Q(cupo_maximo__isnull=True)
                | Q(total_inscriptos_anotado__lt=F('cupo_maximo'))
            )
            .annotate(
                prioridad=Case(
                    When(fecha_inicio__lte=hoy, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            )
            .order_by('prioridad', 'fecha_inicio', '-id')[:5]
        )
        inscripciones_por_mes = (
            inscripciones_periodo.values('anio', 'mes')
            .annotate(cantidad=Count('id'))
            .order_by('anio', 'mes')
        )
        donantes_por_mes = (
            inscripciones_periodo.values('anio', 'mes')
            .annotate(cantidad=Count('usuario_id', distinct=True))
            .order_by('anio', 'mes')
        )

        data = {
            'total_campanias': total_campanias,
            'total_inscripciones': total_inscripciones,
            'total_donantes': total_donantes,
            'campanias_recientes': campanias_recientes,
            'campanias_por_estado': campanias_por_estado,
            'inscripciones_por_mes': inscripciones_por_mes,
            'donantes_por_mes': donantes_por_mes,
        }

        return Response(DashboardSerializer(data).data)
