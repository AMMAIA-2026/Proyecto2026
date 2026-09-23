from datetime import date

from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import RolChoices, Usuario
from .serializers import UsuarioSerializer


class UsuarioTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.usuario = self.crear_usuario(
            email='usuario@example.com',
            username='usuario',
        )
        self.otro_usuario = self.crear_usuario(
            email='otro@example.com',
            username='otro',
        )
        self.client.force_authenticate(self.usuario)

    def crear_usuario(self, **datos):
        return Usuario.objects.create_user(
            password='Password123!',
            nombre='Nombre',
            apellido='Apellido',
            dni=str(10000000 + Usuario.objects.count()),
            fecha_nacimiento=date(1990, 1, 1),
            rol=RolChoices.USUARIO_ESTANDAR,
            **datos,
        )

    def datos_usuario(self, email, dni='12345678'):
        return {
            'username': 'nuevo',
            'email': email,
            'password': 'Password123!',
            'dni': dni,
            'nombre': 'Nuevo',
            'apellido': 'Usuario',
            'fecha_nacimiento': '1990-01-01',
        }

    def test_email_duplicado_tiene_mensaje_neutro(self):
        serializer = UsuarioSerializer(
            data=self.datos_usuario(self.usuario.email),
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['email'][0]),
            'El correo electrónico ya está registrado.',
        )

    def test_dni_duplicado_tiene_mensaje_neutro(self):
        serializer = UsuarioSerializer(
            data=self.datos_usuario(
                'nuevo@example.com',
                dni=self.usuario.dni,
            ),
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['dni'][0]),
            'El DNI ya está registrado.',
        )

    def test_usuario_no_puede_acceder_a_datos_de_otro_usuario(self):
        response = self.client.get(
            reverse(
                'usuario-detail',
                kwargs={'usuario_id': self.otro_usuario.id},
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['codigo'], 'permiso_denegado')
        self.assertEqual(
            response.json()['mensaje'],
            'No tenés permisos para acceder a este recurso.',
        )

    def test_usuario_puede_acceder_a_sus_propios_datos(self):
        response = self.client.get(
            reverse(
                'usuario-detail',
                kwargs={'usuario_id': self.usuario.id},
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.usuario.id)

    def test_usuario_inexistente_responde_404(self):
        response = self.client.get(
            reverse('usuario-detail', kwargs={'usuario_id': 999999}),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
