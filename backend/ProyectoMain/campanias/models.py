from django.db import models
from django.core.validators import MinValueValidator

class EstadoCampaniaChoices(models.TextChoices):
    ACTIVA = 'Activa', 'Activa'
    FINALIZADA = 'Finalizada', 'Finalizada'
    PROXIMAMENTE = 'Proximamente', 'Próximamente'

class Campania(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1500)
    ubicacion = models.CharField(max_length=100)
    centro_salud = models.ForeignKey(
        'centros_salud.CentroSalud',
        on_delete=models.PROTECT,
        related_name='campanias',
        null=True,
        blank=True,
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cupo_maximo = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    estado_campania = models.CharField(
        max_length=12,
        choices=EstadoCampaniaChoices.choices,
        null=False,
        blank=False
    )

    class Meta:
        db_table = 'campanias'

    def __str__(self):
        return self.titulo



    

    
