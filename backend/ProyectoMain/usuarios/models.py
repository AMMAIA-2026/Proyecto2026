from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class RolChoices(models.TextChoices):
    ADMINISTRADOR = 'Administrador', 'Administrador'
    USUARIO_ESTANDAR = 'Usuario Estandar', 'Usuario Estandar'

class GrupoSanguineoChoices(models.TextChoices):
    A_POSITIVO = 'A+', 'A+'
    A_NEGATIVO = 'A-', 'A-'
    B_POSITIVO = 'B+', 'B+'
    B_NEGATIVO = 'B-', 'B-'
    AB_POSITIVO = 'AB+', 'AB+'
    AB_NEGATIVO = 'AB-', 'AB-'
    O_POSITIVO = 'O+', 'O+'
    O_NEGATIVO = 'O-', 'O-'


LETRAS_NOMBRE_REGEX = r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñÜü]+)*$"


class Usuario(AbstractUser):

    email = models.EmailField(unique=True)  
    
    USERNAME_FIELD = 'email'               
    REQUIRED_FIELDS = ['username', 'nombre', 'apellido'] 

    dni = models.CharField(validators=[
        RegexValidator(
            regex=r'^\d{7,8}$',
            message='El DNI debe contener entre 7 y 8 dígitos.'
        )
    ], max_length=8, unique=True)
    nombre = models.CharField(
        max_length=25,
        validators=[
            RegexValidator(
                regex=LETRAS_NOMBRE_REGEX,
                message='El nombre solo puede contener letras, tildes y espacios.'
            )
        ]
    )
    apellido = models.CharField(
        max_length=25,
        validators=[
            RegexValidator(
                regex=LETRAS_NOMBRE_REGEX,
                message='El apellido solo puede contener letras, tildes y espacios.'
            )
        ]
    )
    fecha_nacimiento = models.DateField()
    fecha_registro = models.DateField(auto_now_add=True)

    rol = models.CharField(
        max_length=16,
        choices=RolChoices.choices,
        null=False,
        blank=False
    )
    grupo_sanguineo = models.CharField(
        max_length=3,
        choices=GrupoSanguineoChoices.choices,
        null=False,
        blank=False
    )

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
