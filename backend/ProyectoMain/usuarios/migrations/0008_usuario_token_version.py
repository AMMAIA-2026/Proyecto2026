from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0007_cargar_usuarios_deploy'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='token_version',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
