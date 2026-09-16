from django.db import migrations, models


ESTADOS_VALIDOS = {
    'Activa',
    'Finalizada',
    'Proximamente',
}


def copiar_estados_a_choices(apps, schema_editor):
    Campania = apps.get_model('campanias', 'Campania')
    EstadoCampania = apps.get_model('campanias', 'Estado_Campania')

    estados = dict(
        EstadoCampania.objects.values_list('id', 'estado')
    )

    for campania in Campania.objects.all().iterator():
        estado = estados.get(campania.estado_campania_id)

        if estado not in ESTADOS_VALIDOS:
            raise ValueError(
                f'La campaña {campania.pk} tiene un estado no permitido: {estado!r}'
            )

        campania.estado_campania_enum_tmp = estado
        campania.save(update_fields=['estado_campania_enum_tmp'])


class Migration(migrations.Migration):

    dependencies = [
        ('campanias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campania',
            name='estado_campania_enum_tmp',
            field=models.CharField(
                blank=True,
                choices=[
                    ('Activa', 'Activa'),
                    ('Finalizada', 'Finalizada'),
                    ('Proximamente', 'Próximamente'),
                ],
                max_length=12,
                null=True,
            ),
        ),
        migrations.RunPython(
            copiar_estados_a_choices,
            migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='campania',
            name='estado_campania',
        ),
        migrations.RenameField(
            model_name='campania',
            old_name='estado_campania_enum_tmp',
            new_name='estado_campania',
        ),
        migrations.AlterField(
            model_name='campania',
            name='estado_campania',
            field=models.CharField(
                blank=False,
                choices=[
                    ('Activa', 'Activa'),
                    ('Finalizada', 'Finalizada'),
                    ('Proximamente', 'Próximamente'),
                ],
                max_length=12,
                null=False,
            ),
        ),
        migrations.DeleteModel(
            name='Estado_Campania',
        ),
    ]
