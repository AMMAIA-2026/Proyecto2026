from django.db import migrations, models


TELEFONOS_PRINCIPALES = {
    1: '3512480189',
    2: '3514276240',
    3: '3514334121',
    4: '3514807373',
    5: '3547429282',
    6: '3534421003',
    7: '3468433974',
    8: '3549426747',
    9: '3521479579',
    10: '2336494107',
    11: '3525426703',
    12: '3584422295',
    13: '3385453242',
    14: '3472422820',
    15: None,
    16: '3584678700',
    17: '3571410210',
    18: '3564443722',
    19: '3546426671',
    20: '3574480914',
    21: '8005554141',
    22: '3541489676',
    23: '3544426437',
    24: '3534619138',
    25: '3573424704',
}


def normalizar_telefonos(apps, schema_editor):
    CentroSalud = apps.get_model('centros_salud', 'CentroSalud')
    for centro_id, telefono in TELEFONOS_PRINCIPALES.items():
        CentroSalud.objects.filter(pk=centro_id).update(telefono=telefono)


class Migration(migrations.Migration):
    dependencies = [
        ('centros_salud', '0002_cargar_centros'),
    ]

    operations = [
        migrations.RunPython(normalizar_telefonos, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='centrosalud',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='centrosalud',
            name='direccion',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='centrosalud',
            name='barrio',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='centrosalud',
            name='localidad',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='centrosalud',
            name='telefono',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='centrosalud',
            name='sitio_web',
            field=models.URLField(blank=True, max_length=200, null=True),
        ),
    ]
