from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('campanias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CentroSalud',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('nombre', models.CharField(max_length=150)),
                ('direccion', models.CharField(max_length=150)),
                ('barrio', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=50)),
                ('sitio_web', models.URLField(blank=True, max_length=250)),
                ('latitud', models.CharField(blank=True, max_length=30)),
                ('longitud', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='campania',
            name='centro_salud',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='campanias.centrosalud',
            ),
        ),
        migrations.AddField(
            model_name='campania',
            name='cupo_maximo',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
