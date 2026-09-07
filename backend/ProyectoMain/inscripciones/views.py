from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from campanias.models import Campania, EstadoCampaniaChoices
from usuarios.permissions import EsUsuarioEstandar
from .models import Inscripcion
from .serializers import InscripcionSerializer


@api_view(['POST'])
@permission_classes([EsUsuarioEstandar])
def inscribirse_campania(request, campania_id):
    hoy = timezone.localdate()
    nacimiento = request.user.fecha_nacimiento
    edad = hoy.year - nacimiento.year - (
        (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day)
    )
    if edad < 18:
        return Response({
            'codigo': 'edad_no_permitida',
            'mensaje': 'Debés tener al menos 18 años para inscribirte.',
        }, status=status.HTTP_400_BAD_REQUEST)
    if edad >= 65:
        return Response({
            'codigo': 'edad_no_permitida',
            'mensaje': 'Debés tener menos de 65 años para inscribirte.',
        }, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        campania = get_object_or_404(
            Campania.objects.select_for_update(),
            pk=campania_id,
        )
        if campania.fecha_fin < hoy:
            return Response({
                'codigo': 'campania_finalizada',
                'mensaje': 'No podés inscribirte en una campaña finalizada.',
            }, status=status.HTTP_400_BAD_REQUEST)

        if Inscripcion.objects.filter(
            usuario=request.user,
            campania=campania,
        ).exists():
            return Response({
                'codigo': 'inscripcion_duplicada',
                'mensaje': 'Ya estás inscripto en esta campaña.',
            }, status=status.HTTP_409_CONFLICT)

        total = Inscripcion.objects.filter(campania=campania).count()
        if campania.cupo_maximo is not None and total >= campania.cupo_maximo:
            if campania.estado_campania != EstadoCampaniaChoices.FINALIZADA:
                campania.estado_campania = EstadoCampaniaChoices.FINALIZADA
                campania.save(update_fields=['estado_campania'])
            return Response({
                'codigo': 'cupo_completo',
                'mensaje': 'La campaña alcanzó el cupo máximo de donantes.',
            }, status=status.HTTP_409_CONFLICT)

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


@api_view(['GET'])
@permission_classes([AllowAny])
def total_inscriptos(request, campania_id):
    campania = get_object_or_404(Campania, pk=campania_id)
    total = Inscripcion.objects.filter(campania=campania).count()
    return Response({'totalInscriptos': total})
