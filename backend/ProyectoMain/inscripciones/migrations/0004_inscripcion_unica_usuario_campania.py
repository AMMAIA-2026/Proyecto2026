from django.db import migrations, models
from django.db.models import Count, Min


def eliminar_duplicados(apps, schema_editor):
    Inscripcion = apps.get_model('inscripciones', 'Inscripcion')
    duplicados = (
        Inscripcion.objects
        .values('usuario_id', 'campania_id')
        .annotate(cantidad=Count('id'), primera_id=Min('id'))
        .filter(cantidad__gt=1)
    )

    for duplicado in duplicados:
        Inscripcion.objects.filter(
            usuario_id=duplicado['usuario_id'],
            campania_id=duplicado['campania_id'],
        ).exclude(pk=duplicado['primera_id']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('inscripciones', '0003_alter_inscripcion_table'),
    ]

    operations = [
        migrations.RunPython(eliminar_duplicados, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='inscripcion',
            constraint=models.UniqueConstraint(
                fields=('usuario', 'campania'),
                name='inscripcion_unica_usuario_campania',
            ),
        ),
    ]
