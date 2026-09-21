from datetime import date

from django.contrib.auth.hashers import make_password
from django.db import migrations


CONTRASENA_DEPLOY = 'Qwerty123.'

USUARIOS_DEPLOY = [
    {
        'email': 'melinauser@unmail.com',
        'dni': '50123401',
        'nombre': 'Melina',
        'apellido': 'User',
        'fecha_nacimiento': date(1988, 1, 15),
        'rol': 'Usuario Estandar',
    },
    {
        'email': 'melinaadmin@unmail.com',
        'dni': '50123402',
        'nombre': 'Melina',
        'apellido': 'Admin',
        'fecha_nacimiento': date(1988, 2, 16),
        'rol': 'Administrador',
    },
    {
        'email': 'guillermouser@unmail.com',
        'dni': '50123403',
        'nombre': 'Guillermo',
        'apellido': 'User',
        'fecha_nacimiento': date(1989, 3, 17),
        'rol': 'Usuario Estandar',
    },
    {
        'email': 'guillermoadmin@unmail.com',
        'dni': '50123404',
        'nombre': 'Guillermo',
        'apellido': 'Admin',
        'fecha_nacimiento': date(1989, 4, 18),
        'rol': 'Administrador',
    },
    {
        'email': 'astriduser@unmail.com',
        'dni': '50123405',
        'nombre': 'Astrid',
        'apellido': 'User',
        'fecha_nacimiento': date(1990, 5, 19),
        'rol': 'Usuario Estandar',
    },
    {
        'email': 'astridadmin@unmail.com',
        'dni': '50123406',
        'nombre': 'Astrid',
        'apellido': 'Admin',
        'fecha_nacimiento': date(1990, 6, 20),
        'rol': 'Administrador',
    },
    {
        'email': 'irinauser@unmail.com',
        'dni': '50123407',
        'nombre': 'Irina',
        'apellido': 'User',
        'fecha_nacimiento': date(1991, 7, 21),
        'rol': 'Usuario Estandar',
    },
    {
        'email': 'irinaadmin@unmail.com',
        'dni': '50123408',
        'nombre': 'Irina',
        'apellido': 'Admin',
        'fecha_nacimiento': date(1991, 8, 22),
        'rol': 'Administrador',
    },
    {
        'email': 'abigailuser@unmail.com',
        'dni': '50123409',
        'nombre': 'Abigail',
        'apellido': 'User',
        'fecha_nacimiento': date(1992, 9, 23),
        'rol': 'Usuario Estandar',
    },
    {
        'email': 'abigailadmin@unmail.com',
        'dni': '50123410',
        'nombre': 'Abigail',
        'apellido': 'Admin',
        'fecha_nacimiento': date(1992, 10, 24),
        'rol': 'Administrador',
    },
    {
        'email': 'marcelauser@unmail.com',
        'dni': '50123411',
        'nombre': 'Marcela',
        'apellido': 'User',
        'fecha_nacimiento': date(1993, 11, 25),
        'rol': 'Usuario Estandar',
    },
    {
        'email': 'marcelaadmin@unmail.com',
        'dni': '50123412',
        'nombre': 'Marcela',
        'apellido': 'Admin',
        'fecha_nacimiento': date(1993, 12, 26),
        'rol': 'Administrador',
    },
]


def cargar_usuarios_deploy(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')

    for datos in USUARIOS_DEPLOY:
        Usuario.objects.get_or_create(
            email=datos['email'],
            defaults={
                **datos,
                'username': datos['email'],
                'password': make_password(CONTRASENA_DEPLOY),
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0006_eliminar_grupo_sanguineo'),
    ]

    operations = [
        migrations.RunPython(
            cargar_usuarios_deploy,
            migrations.RunPython.noop,
        ),
    ]
