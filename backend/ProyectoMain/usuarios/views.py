from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Usuario, RolChoices
from .serializers import (
    CustomTokenObtainPairSerializer,
    RecuperarPasswordSerializer,
    UsuarioSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from usuarios.permissions import EsAdministradorOSiMismo

class UsuarioQuerysetMixin:
    permission_classes = [EsAdministradorOSiMismo]

    def get_queryset(self, request):
        if request.user.rol == RolChoices.ADMINISTRADOR:
            return Usuario.objects.all()
        return Usuario.objects.filter(pk=request.user.pk)

    def get_object(self, request, usuario_id):
        usuario = get_object_or_404(
            self.get_queryset(request),
            pk=usuario_id,
        )
        self.check_object_permissions(request, usuario)
        return usuario


class UsuarioListView(UsuarioQuerysetMixin, APIView):
    def get(self, request):
        serializer = UsuarioSerializer(
            self.get_queryset(request),
            many=True,
        )
        return Response(serializer.data)


class UsuarioDetailView(UsuarioQuerysetMixin, APIView):
    def get(self, request, usuario_id):
        usuario = self.get_object(request, usuario_id)
        return Response(UsuarioSerializer(usuario).data)

    def put(self, request, usuario_id):
        usuario = self.get_object(request, usuario_id)
        serializer = UsuarioSerializer(usuario, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, usuario_id):
        usuario = self.get_object(request, usuario_id)
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistroView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Usuario registrado correctamente'},
                status=status.HTTP_201_CREATED,
            )
        errores = dict(serializer.errors)
        errores['codigo'] = 'validacion_invalida'
        errores['status_code'] = status.HTTP_400_BAD_REQUEST
        return Response(errores, status=status.HTTP_400_BAD_REQUEST)


class RecuperarPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RecuperarPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        usuario = Usuario.objects.filter(email__iexact=email).first()

        if usuario:
            usuario.set_password(password)
            usuario.save(update_fields=['password'])

        return Response({
            'message': (
                'Si existe una cuenta asociada a ese email, la contraseña fue '
                'actualizada. Ya podés intentar iniciar sesión.'
            )
        })

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

