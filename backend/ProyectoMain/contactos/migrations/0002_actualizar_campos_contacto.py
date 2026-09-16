from django.db import migrations, models


MOTIVOS_VALIDOS = {
    'Consulta general',
    'Problema técnico',
    'Sugerencia',
    'Otro',
}


def normalizar_motivos_existentes(apps, schema_editor):
    Contacto = apps.get_model('contactos', 'Contacto')
    Contacto.objects.exclude(motivo__in=MOTIVOS_VALIDOS).update(motivo='Otro')


class Migration(migrations.Migration):
    dependencies = [
        ('contactos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='nombre_completo',
            field=models.CharField(default='Sin especificar', max_length=100),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='contacto',
            old_name='email',
            new_name='correo_electronico',
        ),
        migrations.RenameField(
            model_name='contacto',
            old_name='asunto',
            new_name='motivo',
        ),
        migrations.RunPython(normalizar_motivos_existentes, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='contacto',
            name='motivo',
            field=models.CharField(
                choices=[
                    ('Consulta general', 'Consulta general'),
                    ('Problema técnico', 'Problema técnico'),
                    ('Sugerencia', 'Sugerencia'),
                    ('Otro', 'Otro'),
                ],
                max_length=30,
            ),
        ),
    ]
