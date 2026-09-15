from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CentroSalud
from .serializers import CentroSaludSerializer


class CentroSaludListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = CentroSaludSerializer(
            CentroSalud.objects.all(),
            many=True,
        )
        return Response(serializer.data)
