import django.core.validators
from django.db import migrations, models


ROLES_VALIDOS = {
    'Administrador',
    'Usuario Estandar',
}

GRUPOS_VALIDOS = {
    'A+',
    'A-',
    'B+',
    'B-',
    'AB+',
    'AB-',
    'O+',
    'O-',
}


def validar_datos_legacy(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')
    Rol = apps.get_model('usuarios', 'Rol')
    GrupoSanguineo = apps.get_model('usuarios', 'GrupoSanguineo')

    roles = dict(Rol.objects.values_list('id', 'tipo_rol'))
    grupos = {
        pk: f'{grupo}{factor}'
        for pk, grupo, factor in GrupoSanguineo.objects.values_list(
            'id',
            'grupo',
            'factor'
        )
    }

    for usuario in Usuario.objects.all().iterator():
        rol = roles.get(usuario.rol_id)
        grupo = grupos.get(usuario.grupo_sanguineo_id)

        if rol not in ROLES_VALIDOS:
            raise ValueError(
                f'El usuario {usuario.pk} tiene un rol no permitido: {rol!r}'
            )

        if grupo not in GRUPOS_VALIDOS:
            raise ValueError(
                f'El usuario {usuario.pk} tiene un grupo sanguíneo no permitido: {grupo!r}'
            )


def copiar_valores_a_choices(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')
    Rol = apps.get_model('usuarios', 'Rol')
    GrupoSanguineo = apps.get_model('usuarios', 'GrupoSanguineo')

    roles = dict(Rol.objects.values_list('id', 'tipo_rol'))
    grupos = {
        pk: f'{grupo}{factor}'
        for pk, grupo, factor in GrupoSanguineo.objects.values_list(
            'id',
            'grupo',
            'factor'
        )
    }

    for usuario in Usuario.objects.all().iterator():
        rol = roles.get(usuario.rol_id)
        grupo = grupos.get(usuario.grupo_sanguineo_id)

        if rol not in ROLES_VALIDOS:
            raise ValueError(
                f'El usuario {usuario.pk} tiene un rol no permitido: {rol!r}'
            )

        if grupo not in GRUPOS_VALIDOS:
            raise ValueError(
                f'El usuario {usuario.pk} tiene un grupo sanguíneo no permitido: {grupo!r}'
            )

        usuario.rol_enum_tmp = rol
        usuario.grupo_sanguineo_enum_tmp = grupo
        usuario.save(
            update_fields=[
                'rol_enum_tmp',
                'grupo_sanguineo_enum_tmp'
            ]
        )


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_usuario_email'),
    ]

    operations = [
        migrations.RunPython(
            validar_datos_legacy,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='dni',
            field=models.CharField(
                max_length=8,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message='El DNI debe contener entre 7 y 8 dígitos.',
                        regex='^\\d{7,8}$',
                    ),
                ],
            ),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='apellido',
            field=models.CharField(max_length=25),
        ),
        migrations.AddField(
            model_name='usuario',
            name='rol_enum_tmp',
            field=models.CharField(
                blank=True,
                choices=[
                    ('Administrador', 'Administrador'),
                    ('Usuario Estandar', 'Usuario Estandar'),
                ],
                max_length=16,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='usuario',
            name='grupo_sanguineo_enum_tmp',
            field=models.CharField(
                blank=True,
                choices=[
                    ('A+', 'A+'),
                    ('A-', 'A-'),
                    ('B+', 'B+'),
                    ('B-', 'B-'),
                    ('AB+', 'AB+'),
                    ('AB-', 'AB-'),
                    ('O+', 'O+'),
                    ('O-', 'O-'),
                ],
                max_length=3,
                null=True,
            ),
        ),
        migrations.RunPython(
            copiar_valores_a_choices,
            migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='rol',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='grupo_sanguineo',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='rol_enum_tmp',
            new_name='rol',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='grupo_sanguineo_enum_tmp',
            new_name='grupo_sanguineo',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(
                blank=False,
                choices=[
                    ('Administrador', 'Administrador'),
                    ('Usuario Estandar', 'Usuario Estandar'),
                ],
                max_length=16,
                null=False,
            ),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='grupo_sanguineo',
            field=models.CharField(
                blank=False,
                choices=[
                    ('A+', 'A+'),
                    ('A-', 'A-'),
                    ('B+', 'B+'),
                    ('B-', 'B-'),
                    ('AB+', 'AB+'),
                    ('AB-', 'AB-'),
                    ('O+', 'O+'),
                    ('O-', 'O-'),
                ],
                max_length=3,
                null=False,
            ),
        ),
        migrations.DeleteModel(
            name='Rol',
        ),
        migrations.DeleteModel(
            name='GrupoSanguineo',
        ),
    ]
