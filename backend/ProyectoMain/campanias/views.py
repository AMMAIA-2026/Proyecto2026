from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import status
from .models import Campania
from .serializers import CampaniaSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from usuarios.permissions import EsAdministrador

@api_view(['GET'])
@permission_classes([AllowAny])
def campania_activa(request):
    campania = Campania.objects.order_by('fecha_inicio').first()
    if not campania:
        return Response({'error': 'No hay campañas.'}, status=404)
    return Response(CampaniaSerializer(campania).data)


class CampaniaListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [EsAdministrador()]

    def get(self, request):
        campanias = (
            Campania.objects
            .select_related('centro_salud')
            .annotate(total_inscriptos_anotado=Count('inscripcion'))
        )
        return Response(CampaniaSerializer(campanias, many=True).data)

    def post(self, request):
        serializer = CampaniaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CampaniaDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [EsAdministrador()]

    def get_object(self, campania_id):
        queryset = (
            Campania.objects
            .select_related('centro_salud')
            .annotate(total_inscriptos_anotado=Count('inscripcion'))
        )
        return get_object_or_404(queryset, pk=campania_id)

    def get(self, request, campania_id):
        campania = self.get_object(campania_id)
        return Response(CampaniaSerializer(campania).data)

    def put(self, request, campania_id):
        campania = self.get_object(campania_id)
        serializer = CampaniaSerializer(campania, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, campania_id):
        campania = self.get_object(campania_id)
        serializer = CampaniaSerializer(
            campania,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, campania_id):
        campania = self.get_object(campania_id)
        campania.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
