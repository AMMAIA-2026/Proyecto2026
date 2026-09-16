from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from usuarios.permissions import EsAdministrador
from .models import Contacto
from .serializers import ContactoSerializer, ContactoTrackedSerializer


class ContactoListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [EsAdministrador()]

    def post(self, request):
            serializer = ContactoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        contactos = Contacto.objects.all()
        serializer = ContactoSerializer(contactos, many=True)
        return Response(serializer.data)


class ContactoDetailView(APIView):
    permission_classes = [EsAdministrador]

    def get(self, request, contacto_id):
        contacto = get_object_or_404(Contacto, pk=contacto_id)
        return Response(ContactoSerializer(contacto).data)

    def put(self, request, contacto_id):
        contacto = get_object_or_404(Contacto, pk=contacto_id)
        serializer = ContactoTrackedSerializer(
            contacto,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ContactoSerializer(contacto).data)
