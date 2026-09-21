from django.db import transaction
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from campanias.models import Campania, EstadoCampaniaChoices
from campanias.serializers import CampaniaSerializer
from usuarios.permissions import EsAdministrador, EsUsuarioEstandar
from .models import Inscripcion
from .serializers import (
    InscripcionPropiaSerializer,
    InscripcionSerializer,
    UsuarioInscripcionSerializer,
)


def error_response(codigo, mensaje, http_status):
    return Response({
        'codigo': codigo,
        'mensaje': mensaje,
        'status_code': http_status,
    }, status=http_status)


class InscribirseCampaniaView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [EsAdministrador()]
        return [EsUsuarioEstandar()]

    def get(self, request, campania_id):
        campania = get_object_or_404(
            Campania.objects
            .select_related('centro_salud')
            .annotate(total_inscriptos_anotado=Count('inscripcion')),
            pk=campania_id,
        )
        inscripciones = Inscripcion.objects.filter(
            campania=campania,
        ).select_related('usuario').order_by(
            'usuario__apellido',
            'usuario__nombre',
        )
        total_inscriptos = inscripciones.count()

        busqueda = request.query_params.get('buscar', '').strip()
        if busqueda:
            inscripciones = inscripciones.filter(
                Q(usuario__nombre__icontains=busqueda)
                | Q(usuario__apellido__icontains=busqueda)
                | Q(usuario__dni__icontains=busqueda)
                | Q(usuario__email__icontains=busqueda)
            )

        return Response({
            'campania': CampaniaSerializer(campania).data,
            'total_inscriptos': total_inscriptos,
            'usuarios': UsuarioInscripcionSerializer(
                [inscripcion.usuario for inscripcion in inscripciones],
                many=True,
            ).data,
        })

    def post(self, request, campania_id):
        hoy = timezone.localdate()
        nacimiento = request.user.fecha_nacimiento
        edad = hoy.year - nacimiento.year - (
            (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day)
        )
        if edad < 18:
            return error_response(
                'edad_no_permitida',
                'Debés tener al menos 18 años para inscribirte.',
                status.HTTP_400_BAD_REQUEST,
            )
        if edad >= 65:
            return error_response(
                'edad_no_permitida',
                'Debés tener menos de 65 años para inscribirte.',
                status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            campania = get_object_or_404(
                Campania.objects.select_for_update(),
                pk=campania_id,
            )
            if campania.fecha_fin < hoy:
                return error_response(
                    'campania_finalizada',
                    'No podés inscribirte en una campaña finalizada.',
                    status.HTTP_400_BAD_REQUEST,
                )

            if Inscripcion.objects.filter(
                usuario=request.user,
                campania=campania,
            ).exists():
                return error_response(
                    'inscripcion_duplicada',
                    'Ya estás inscripto en esta campaña.',
                    status.HTTP_409_CONFLICT,
                )

            total = Inscripcion.objects.filter(campania=campania).count()
            if campania.cupo_maximo is not None and total >= campania.cupo_maximo:
                if campania.estado_campania != EstadoCampaniaChoices.FINALIZADA:
                    campania.estado_campania = EstadoCampaniaChoices.FINALIZADA
                    campania.save(update_fields=['estado_campania'])
                return error_response(
                    'cupo_completo',
                    'La campaña alcanzó el cupo máximo de donantes.',
                    status.HTTP_409_CONFLICT,
                )

            inscripcion = Inscripcion.objects.create(
                usuario=request.user,
                campania=campania,
            )
            total += 1
            if campania.cupo_maximo is not None and total >= campania.cupo_maximo:
                campania.estado_campania = EstadoCampaniaChoices.FINALIZADA
                campania.save(update_fields=['estado_campania'])

        return Response({
            'data': InscripcionSerializer(inscripcion).data,
            'totalInscriptos': total,
        }, status=status.HTTP_201_CREATED)


class MisInscripcionesView(APIView):
    permission_classes = [EsUsuarioEstandar]

    def get(self, request):
        inscripciones = Inscripcion.objects.filter(
            usuario=request.user,
        ).select_related('campania__centro_salud').order_by(
            'campania__fecha_inicio',
            '-id',
        )

        actuales = []
        historicas = []

        for inscripcion in inscripciones:
            estado = CampaniaSerializer.calcular_estado(
                inscripcion.campania.fecha_inicio,
                inscripcion.campania.fecha_fin,
                inscripcion.campania.cupo_maximo,
                inscripcion.campania.inscripcion_set.count(),
            )
            serialized = InscripcionPropiaSerializer(inscripcion).data
            if estado == EstadoCampaniaChoices.FINALIZADA:
                historicas.append(serialized)
            else:
                actuales.append(serialized)

        return Response({
            'actuales': actuales,
            'historicas': historicas,
        })


class CancelarInscripcionView(APIView):
    permission_classes = [EsUsuarioEstandar]

    def delete(self, request, inscripcion_id):
        inscripcion = get_object_or_404(
            Inscripcion.objects.select_related('campania'),
            pk=inscripcion_id,
            usuario=request.user,
        )
        campania = inscripcion.campania
        estado = CampaniaSerializer.calcular_estado(
            campania.fecha_inicio,
            campania.fecha_fin,
            campania.cupo_maximo,
            campania.inscripcion_set.count(),
        )

        if estado == EstadoCampaniaChoices.FINALIZADA:
            return error_response(
                'campania_finalizada',
                'No podés cancelar una inscripción de una campaña finalizada.',
                status.HTTP_400_BAD_REQUEST,
            )

        inscripcion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
