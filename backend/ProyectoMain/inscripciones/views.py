from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from campanias.models import Campania, EstadoCampaniaChoices
from usuarios.permissions import EsUsuarioEstandar
from .models import Inscripcion
from .serializers import InscripcionSerializer


def error_response(codigo, mensaje, http_status):
    return Response({
        'codigo': codigo,
        'mensaje': mensaje,
        'status_code': http_status,
    }, status=http_status)


class InscribirseCampaniaView(APIView):
    permission_classes = [EsUsuarioEstandar]

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
