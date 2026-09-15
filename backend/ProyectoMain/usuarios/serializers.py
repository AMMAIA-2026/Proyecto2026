from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.validators import RegexValidator
from .models import Usuario, RolChoices
from django.contrib.auth import authenticate


VALIDADORES_PASSWORD = [
    RegexValidator(
        regex=r'[A-Z]',
        message='La contraseña debe contener al menos una mayúscula.'
    ),
    RegexValidator(
        regex=r'[a-z]',
        message='La contraseña debe contener al menos una minúscula.'
    ),
    RegexValidator(
        regex=r'[0-9]',
        message='La contraseña debe contener al menos un número.'
    ),
    RegexValidator(
        regex=r'[^A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9\s]',
        message='La contraseña debe contener al menos un carácter especial.'
    ),
]


def campo_password():
    return serializers.CharField(
        write_only=True,
        min_length=10,
        error_messages={
            'min_length': 'La contraseña debe tener al menos 10 caracteres.'
        },
        validators=VALIDADORES_PASSWORD,
    )


class UsuarioSerializer(serializers.ModelSerializer):

    password = campo_password()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['password'].required = False

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'password',  
            'dni',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'fecha_registro',
            'rol',
            'grupo_sanguineo',
        ]
        read_only_fields = [
            'rol',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['rol'] = RolChoices.USUARIO_ESTANDAR
        user = Usuario(**validated_data)
        user.set_password(password)  
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('rol', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save(update_fields=['password'])

        return user


class RecuperarPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = campo_password()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            username=email,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                'Credenciales incorrectas',
                code='credenciales_incorrectas',
            )

        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),

            'user': {
                'id': user.id,
                'email': user.email,
                'rol': user.rol
            }
        }

        return data

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        token['id'] = user.id
        token['email'] = user.email
        token['rol'] = user.rol

        return token
