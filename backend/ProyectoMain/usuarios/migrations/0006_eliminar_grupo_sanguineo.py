from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0005_usuario_fecha_nacimiento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='grupo_sanguineo',
        ),
    ]
