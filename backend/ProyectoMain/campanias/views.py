from django.shortcuts import render
from rest_framework import viewsets
from .models import Campania, Estado_Campania
from inscripciones.models import Inscripcion
from .serializers import CampaniaSerializer, EstadoCampaniaSerializer
from datetime import date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from usuarios.permissions import EsAdministrador

@api_view(['GET'])
@permission_classes([AllowAny])
def campania_activa(request):
    campania = Campania.objects.order_by('fecha_inicio').first()

    if not campania:
        return Response({'error': 'No hay campañas.'}, status=404)

    return Response(CampaniaSerializer(campania).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def inscribirse_campania(request, campania_id):

    Inscripcion.objects.create(
        usuario=request.user,
        campania_id=campania_id,
        fecha_inscripcion=timezone.now()
    )

    return Response({"mensaje": "Inscripción correcta"})

class CampaniaViewSet(viewsets.ModelViewSet):

    queryset = Campania.objects.select_related('centro_salud').all()
    serializer_class = CampaniaSerializer

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [EsAdministrador]

        return [permission() for permission in permission_classes]

class EstadoCampaniaViewSet(viewsets.ModelViewSet):

    queryset = Estado_Campania.objects.all()
    serializer_class = EstadoCampaniaSerializer
